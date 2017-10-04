// throw a 409 exception which is not defined by org.mule.module.apikit.exception.

// I want to extend MuleRestException but I can't find it!
// import org.mule.module.apikit.api.exception.MuleRestException;

public class PatchConflictException extends Exception {
	private static final long serialVersionUID = 1L;

	public PatchConflictException(String message) {
		super(message);
	}
	public PatchConflictException(String message, Throwable t) {
		super(message, t);
	}
	public PatchConflictException(Throwable t) {
		super(t);
	}
}
