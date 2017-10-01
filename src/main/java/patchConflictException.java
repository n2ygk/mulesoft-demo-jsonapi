// throw a 409 exception which is not defined by org.mule.module.apikit.exception.

// package org.mule.module.apikit.exception;
// import org.mule.module.apikit.api.exception.MuleRestException;

public class patchConflictException extends Exception {
    public patchConflictException(String message) {
        super(message);
    }
}