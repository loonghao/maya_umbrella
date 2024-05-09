mod text;

use std::{io, path::Path};

use async_trait::async_trait;
use tokio::{fs::File, io::AsyncReadExt};

pub use text::*;

pub trait Specimen {
    fn data(&self) -> &[u8];
    fn mut_data(&mut self) -> &mut [u8];
}

#[async_trait]
pub trait FileSpecimen
where
    Self: Sized + Specimen,
{
    async fn read_file<P: AsRef<Path> + Send>(&mut self, path: P) -> Result<(), io::Error> {
        let mut file = File::open(path).await?;
        file.read_exact(self.mut_data()).await?;

        Ok(())
    }
}
