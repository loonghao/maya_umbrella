use regex::Regex;

use crate::{TextSpecimen, VirusDetector};

impl VirusDetector for TextSpecimen {
    type Signature = str;

    fn detect<T: AsRef<Self::Signature>>(&self, signatures: &[T]) -> bool {
        let signatures = signatures
            .iter()
            .map(|s| Regex::new(s.as_ref()).unwrap())
            .collect::<Vec<_>>();

        signatures
            .into_iter()
            .any(|signature| signature.is_match(self))
    }
}

#[cfg(test)]
mod tests {
    use crate::TextSpecimen;

    use super::*;

    #[test]
    fn should_text_virus_detector_works() {
        let specimen = TextSpecimen::new("import vaccine;vaccine.fuck()");
        assert_eq!(true, specimen.detect(&[r"import vaccine"]));
    }
}
