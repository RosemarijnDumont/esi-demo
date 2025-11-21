
import React, { useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';

const MFAEnrollment = () => {
  const [secretKey, setSecretKey] = useState('');
  const [qrCodeData, setQrCodeData] = useState('');
  const [isEnrolled, setIsEnrolled] = useState(false);

  const generateSecret = async () => {
    // In a real application, this would involve an API call to your backend
    // to generate a secret key and receive the QR code data.
    // For this example, we'll simulate it.
    const newSecret = Array(16).fill(0).map(() => String.fromCharCode(Math.floor(Math.random() * 26) + 97)).join(''); // Placeholder random string
    const data = `otpauth://totp/YourApp:user@example.com?secret=${newSecret}&issuer=YourApp`;
    setSecretKey(newSecret);
    setQrCodeData(data);
  };

  const handleEnrollmentConfirmation = async () => {
    // In a real application, this would involve an API call to confirm enrollment
    // after the user has scanned the QR code and entered a token from their authenticator app.
    setIsEnrolled(true);
    alert('MFA Enrollment Successful!');
  };

  return (
    <div className="mfa-enrollment-container">
      <h2>App-Based MFA Enrollment</h2>
      {!isEnrolled ? (
        <>
          <p>Follow these steps to set up app-based Multi-Factor Authentication:</p>
          <ol>
            <li>Download an authenticator app (e.g., Google Authenticator, Authy) to your mobile device.</li>
            <li>Tap on the '+' icon in the authenticator app and choose 'Scan a QR code'.</li>
            <li>Scan the QR code below:</li>
          </ol>
          <div className="qr-code-display">
            {qrCodeData ? (
              <QRCodeSVG value={qrCodeData} size={256} level="H" />
            ) : (
              <button onClick={generateSecret}>Generate QR Code</button>
            )}
          </div>
          {secretKey && (
            <div className="manual-key-entry">
              <p>Or, if you cannot scan the QR code, enter this key manually:</p>
              <pre><code>{secretKey}</code></pre>
            </div>
          )}
          {qrCodeData && (
            <button onClick={handleEnrollmentConfirmation} className="confirm-button">
              I have scanned the QR code and set up my authenticator app.
            </button>
          )}
        </>
      ) : (
        <div className="enrollment-success">
          <p>You have successfully enrolled in app-based MFA!</p>
          <p>You can now use your authenticator app to log in.</p>
        </div>
      )}
    </div>
  );
};

export default MFAEnrollment;
