"use client";

export function SubmissionSuccessModal({
  title,
  message,
  onClose,
}: {
  title: string;
  message: string;
  onClose: () => void;
}) {
  return (
    <div className="meeting-success-backdrop" role="presentation" onClick={onClose}>
      <div
        className="meeting-success-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="submission-success-title"
        onClick={(event) => event.stopPropagation()}
      >
        <button className="meeting-success-close" type="button" onClick={onClose} aria-label="Close confirmation">×</button>
        <span className="meeting-success-check">✓</span>
        <p>Submission received</p>
        <h2 id="submission-success-title">{title}</h2>
        <div>{message}</div>
        <button className="meeting-success-action" type="button" onClick={onClose}>Done</button>
      </div>
    </div>
  );
}
