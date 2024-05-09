mod text_virus_detector;

pub trait VirusDetector {
    type Signature: ?Sized;

    fn detect<T: AsRef<Self::Signature>>(&self, signatures: &[T]) -> bool;
}
