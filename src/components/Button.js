import React from 'react';
import './Button.css'; // Assuming a generic Button.css for base styles

const Button = ({ children, onClick, type = 'primary', ...props }) => {
  const buttonClass = `button ${type}`;
  return (
    <button className={buttonClass} onClick={onClick} {...props}>
      {children}
    </button>
  );
};

export default Button;
