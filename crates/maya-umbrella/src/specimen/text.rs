use std::{
    fmt::{self, Display, Formatter},
    io,
    ops::Deref,
    path::Path,
};

use async_trait::async_trait;
use encoding_rs::GBK;
use tokio::{fs::File, io::AsyncReadExt};

use crate::{FileSpecimen, Specimen};

#[derive(Debug)]
pub struct TextSpecimen {
    contents: String,
}

impl Specimen for TextSpecimen {
    fn data(&self) -> &[u8] {
        self.contents.as_bytes()
    }

    fn mut_data(&mut self) -> &mut [u8] {
        unsafe { self.contents.as_bytes_mut() }
    }
}

impl TextSpecimen {
    pub fn new(data: impl Into<String>) -> Self {
        Self {
            contents: data.into(),
        }
    }
}

#[async_trait]
impl FileSpecimen for TextSpecimen {
    async fn read_file<P: AsRef<Path> + Send>(&mut self, path: P) -> Result<(), io::Error> {
        let mut file = File::open(path).await?;
        if let Err(e) = file.read_to_string(&mut self.contents).await {
            match e.kind() {
                io::ErrorKind::InvalidData => {
                    let mut buf: Vec<u8> = Vec::new();
                    file.read_to_end(&mut buf).await?;
                    let (decoded, _, _) = GBK.decode(&buf);
                    self.contents = decoded.to_string();
                }
                _ => return Err(e),
            }
        }

        Ok(())
    }
}

impl Default for TextSpecimen {
    fn default() -> Self {
        Self::new(String::new())
    }
}

impl Deref for TextSpecimen {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.contents
    }
}

impl Display for TextSpecimen {
    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        write!(f, "{}", self.contents)
    }
}
