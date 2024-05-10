use cpython::{py_fn, py_module_initializer, PyResult, Python};
use lazy_static::lazy_static;
use maya_umbrella::{FileLoader, FileSpecimenResults, Loader, TextSpecimen, VirusDetector};
use tokio::runtime::Runtime;

lazy_static! {
    static ref TOKIO_RUNTIME: Runtime = Runtime::new().unwrap();
}

fn check_virus_from_file(_: Python, path: &str, signs: Vec<String>) -> PyResult<bool> {
    let res = TOKIO_RUNTIME.block_on(async {
        let file_loader: FileLoader = FileLoader;
        let specimen: TextSpecimen = file_loader.load(path.as_ref()).await.unwrap();
        specimen.detect(&signs)
    });

    Ok(res)
}

fn check_virus_from_files(
    _: Python,
    paths: Vec<String>,
    signs: Vec<String>,
) -> PyResult<Vec<bool>> {
    let res = TOKIO_RUNTIME.block_on(async {
        let file_loader: FileLoader = FileLoader;
        let specimen: FileSpecimenResults<TextSpecimen> =
            file_loader.multiple_load(paths.as_ref()).await;

        specimen
            .into_iter()
            .map(|specimen| match specimen {
                Ok(specimen) => specimen.detect(&signs),
                Err(_) => false,
            })
            .collect::<Vec<_>>()
    });

    Ok(res)
}

py_module_initializer!(maya_umbrella_rs, |py, m| {
    m.add(py, "__doc__", "Maya Umbrella API powered by Rust language")?;
    m.add(
        py,
        "check_virus_from_file",
        py_fn!(py, check_virus_from_file(path: &str, signs: Vec<String>)),
    )?;
    m.add(
        py,
        "check_virus_from_files",
        py_fn!(py, check_virus_from_files(paths: Vec<String>, signs: Vec<String>)),
    )?;
    Ok(())
});
