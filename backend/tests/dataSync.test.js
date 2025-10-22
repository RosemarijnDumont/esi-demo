
const request = require('supertest');
const { app, server } = require('../server'); // Import the Express app and server
const { queue } = require('../src/services/dataSyncService');
const { sendNotification } = require('../src/services/notificationService');
const sinon = require('sinon');

describe('Data Synchronization and Notifications', () => {
  let sendNotificationStub;

  beforeAll((done) => {
    // Clear the queue before tests, if necessary, to prevent interference
    queue.testMode.enter();
    done();
  });

  afterEach(() => {
    queue.testMode.clear(); // Clear jobs after each test
    if (sendNotificationStub) {
      sendNotificationStub.restore(); // Restore original function if stubbed
    }
  });

  afterAll((done) => {
    queue.testMode.exit();
    server.close(done); // Close the server after all tests are done
  });

  describe('POST /api/mobile/sync', () => {
    it('should queue data for synchronization and return 202 status for valid data', async () => {
      const mobileData = { id: 'm123', userId: 'u456', value: 100, timestamp: Date.now() };
      const dataType = 'entry';

      const res = await request(app)
        .post('/api/mobile/sync')
        .send({ data: mobileData, dataType: dataType });

      expect(res.statusCode).toEqual(202);
      expect(res.body.message).toEqual('Data queued for synchronization.');
      expect(res.body.jobId).toBeDefined();
      expect(res.body.status).toEqual('queued');

      // Verify that a job was added to the queue
      expect(queue.testMode.jobs.length).toEqual(1);
      expect(queue.testMode.jobs[0].type).toEqual('processDataSync');
      expect(queue.testMode.jobs[0].data.data).toEqual(mobileData);
      expect(queue.testMode.jobs[0].data.dataType).toEqual(dataType);
    });

    it('should return 400 if data is missing', async () => {
      const res = await request(app)
        .post('/api/mobile/sync')
        .send({ dataType: 'entry' });

      expect(res.statusCode).toEqual(400);
      expect(res.body.message).toEqual('Missing data or dataType.');
    });

    it('should return 400 if dataType is missing', async () => {
      const res = await request(app)
        .post('/api/mobile/sync')
        .send({ data: { id: 'm124' } });

      expect(res.statusCode).toEqual(400);
      expect(res.body.message).toEqual('Missing data or dataType.');
    });

    it('should process the data sync job and send notification', async () => {
      sendNotificationStub = sinon.stub(require('../src/services/notificationService'), 'sendNotification').returns(Promise.resolve({ jobId: 'mockNotifId', status: 'queued' }));

      const mobileData = { id: 'm125', userId: 'u001', value: 200, timestamp: Date.now() };
      const dataType = 'report';

      await request(app)
        .post('/api/mobile/sync')
        .send({ data: mobileData, dataType: dataType });

      // Manually process the job from the test queue
      const job = queue.testMode.jobs[0];
      await new Promise((resolve) => {
        queue.process(job.type, (j, done) => {
            expect(j.data.data).toEqual(mobileData);
            expect(j.data.dataType).toEqual(dataType);
            done();
            resolve();
        });
        queue.testMode.jobs[0].run(); // Simulate running the job
      });
      expect(sendNotificationStub.calledOnce).toBeTruthy();
      expect(sendNotificationStub.calledWith('New report available', mobileData, 'web_client_update')).toBeTruthy();
    });
  });

  describe('POST /api/notify', () => {
    it('should queue an email notification and return 202 status', async () => {
      const emailOptions = { to: 'test@example.com', subject: 'Test Email', text: 'This is a test.' };

      const res = await request(app)
        .post('/api/notify')
        .send({ type: 'email', options: emailOptions });

      expect(res.statusCode).toEqual(202);
      expect(res.body.message).toEqual('Notification queued.');
      expect(res.body.jobId).toBeDefined();
      expect(res.body.status).toEqual('queued');

      expect(queue.testMode.jobs.length).toEqual(1);
      expect(queue.testMode.jobs[0].type).toEqual('sendNotification');
      expect(queue.testMode.jobs[0].data.type).toEqual('email');
      expect(queue.testMode.jobs[0].data.options).toEqual(emailOptions);
    });

    it('should queue an in-app notification and return 202 status', async () => {
      const inAppOptions = { userId: 'user123', message: 'Hello!', data: { key: 'value' } };

      const res = await request(app)
        .post('/api/notify')
        .send({ type: 'in-app', options: inAppOptions });

      expect(res.statusCode).toEqual(202);
      expect(res.body.message).toEqual('Notification queued.');
      expect(res.body.jobId).toBeDefined();
      expect(res.body.status).toEqual('queued');

      expect(queue.testMode.jobs.length).toEqual(1);
      expect(queue.testMode.jobs[0].type).toEqual('sendNotification');
      expect(queue.testMode.jobs[0].data.type).toEqual('in-app');
      expect(queue.testMode.jobs[0].data.options).toEqual(inAppOptions);
    });

    it('should return 400 if notification type is missing', async () => {
      const res = await request(app)
        .post('/api/notify')
        .send({ options: { to: 'test@example.com' } });

      expect(res.statusCode).toEqual(400);
      expect(res.body.message).toEqual('Missing notification type or options.');
    });
  });
});
