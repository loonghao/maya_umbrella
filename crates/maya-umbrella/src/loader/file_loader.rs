use std::{io, path::Path};

use async_trait::async_trait;

use crate::{FileSpecimen, Loader, TextSpecimen};

pub type FileSpecimenResult<T> = Result<T, io::Error>;
pub type FileSpecimenResults<T> = Vec<FileSpecimenResult<T>>;

#[derive(Debug)]
pub struct FileLoader;

pub enum FileType {
    TextFile(TextSpecimen),
}

#[async_trait]
impl<T: FileSpecimen + Default + Send> Loader<T> for FileLoader {
    type Error = io::Error;
    type Option = Path;

    async fn load(&self, option: &Self::Option) -> Result<T, Self::Error> {
        let mut specimen = T::default();
        specimen.read_file(option).await?;
        Ok(specimen)
    }
}

#[async_trait]
impl Loader<FileType> for FileLoader {
    type Error = io::Error;
    type Option = Path;

    async fn load(&self, option: &Self::Option) -> Result<FileType, Self::Error> {
        match option.file_stem().unwrap().to_str().unwrap() {
            // TODO: 区分二进制/文本文件
            _ => {
                let specimen: FileSpecimenResult<TextSpecimen> = self.load(option).await;
                specimen.map(|file| FileType::TextFile(file))
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use std::fs;

    use crate::TextSpecimen;

    use super::*;

    #[tokio::test]
    async fn should_file_loader_works() {
        let file_loader = FileLoader;

        match fs::read_dir("../../tests/data/") {
            Ok(entries) => {
                let paths: Vec<_> = entries
                    .filter_map(|entry| entry.ok().map(|e| e.path()))
                    .collect();

                let res: FileSpecimenResults<TextSpecimen> =
                    file_loader.multiple_load(&paths).await;

                assert_eq!(
                    vec![true, true, true, true, true, true, true],
                    res.into_iter().map(|r| r.is_ok()).collect::<Vec<bool>>()
                );
            }
            _ => {
                assert!(false);
            }
        }
    }
}
