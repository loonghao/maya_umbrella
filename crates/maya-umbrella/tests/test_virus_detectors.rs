use maya_umbrella::{FileLoader, FileSpecimenResults, Loader, TextSpecimen, VirusDetector};
use std::fs;

#[tokio::test]
async fn should_text_virus_detector_works() {
    let file_loader = FileLoader;

    match fs::read_dir("../../tests/data/") {
        Ok(entries) => {
            let paths: Vec<_> = entries
                .filter_map(|entry| entry.ok().map(|e| e.path()))
                .collect();

            let specimens: FileSpecimenResults<TextSpecimen> =
                file_loader.multiple_load(&paths).await;

            let signatures = vec![
                "import vaccine",
                "cmds.evalDeferred.*leukocyte.+",
                "python(.*);.+exec.+(pyCode).+;",
            ];

            assert_eq!(
                vec![false, false, false, true, true, true, true],
                specimens
                    .into_iter()
                    .map(|specimen_res| match specimen_res {
                        Ok(specimen) => specimen.detect(&signatures),
                        Err(e) => panic!("{:?}", e),
                    })
                    .collect::<Vec<_>>()
            );
        }
        _ => {
            assert!(false)
        }
    }
}
