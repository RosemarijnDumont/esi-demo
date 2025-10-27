
const { InfluxDB, Point } = require('@influxdata/influxdb-client');
const { WebClient } = require('@slack/web-api');
require('dotenv').config();

const url = process.env.INFLUXDB_URL;
const token = process.env.INFLUXDB_TOKEN;
const org = process.env.INFLUXDB_ORG;
const bucket = process.env.INFLUXDB_BUCKET;

const slackToken = process.env.SLACK_BOT_TOKEN;
const slackChannel = process.env.SLACK_OAUTH_CHANNEL || '#oauth-alerts';

const influxDB = new InfluxDB({ url, token });
const writeApi = influxDB.getWriteApi(org, bucket);

const slackClient = slackToken ? new WebClient(slackToken) : null;

const recordOAuthError = async ({ timestamp, type, error, description, details }) => {
  try {
    const point = new Point('oauth_callback_errors')
      .tag('error_type', type)
      .stringField('error_code', error || 'N/A')
      .stringField('description', description)
      .stringField('details', JSON.stringify(details))
      .timestamp(timestamp);

    writeApi.writePoint(point);
    await writeApi.flush();
    console.log(`OAuth error recorded: ${description}`);

    // Send Slack alert for critical errors
    if (slackClient && type !== 'client_side_oauth_error' && type !== 'client_side_missing_code') { // Avoid alert spam for minor client-side errors
      await sendSlackAlert(`<!here> *OAuth Callback Failure Alert*\n*Type:* ${type}\n*Error:* ${error || 'N/A'}\n*Description:* ${description}\n*Details:* 

${JSON.stringify(details, null, 2)}`
      );
    }

  } catch (err) {
    console.error('Failed to write OAuth error to InfluxDB or send Slack alert:', err);
  }
};

const recordClientLog = async ({ timestamp, level, component, message, details, userAgent, url }) => {
  try {
    const point = new Point('client_logs')
      .tag('level', level)
      .tag('component', component)
      .stringField('message', message)
      .stringField('details', JSON.stringify(details))
      .stringField('userAgent', userAgent)
      .stringField('url', url)
      .timestamp(timestamp);

    writeApi.writePoint(point);
    await writeApi.flush();
    // console.log(`Client log recorded: ${message}`);

  } catch (err) {
    console.error('Failed to write client log to InfluxDB:', err);
  }
};

const sendSlackAlert = async (message) => {
  if (!slackClient) {
    console.warn('Slack client not initialized. SLACK_BOT_TOKEN might be missing.');
    return;
  }
  try {
    await slackClient.chat.postMessage({
      channel: slackChannel,
      text: message,
    });
    console.log('Slack alert sent.');
  } catch (err) {
    console.error('Failed to send Slack alert:', err);
  }
};

module.exports = { recordOAuthError, recordClientLog };
