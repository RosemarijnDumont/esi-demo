function errorHandler(err, req, res, next) {
    console.error(err.stack); // Log the error stack for debugging
    res.status(500).send({
        message: "An unexpected error occurred.",
        error: process.env.NODE_ENV === 'development' ? err.message : {} // In production, don't leak internal error details
    });
}

module.exports = errorHandler;