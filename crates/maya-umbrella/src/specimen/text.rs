use std::{
    fmt::{self, Display, Formatter},
    ops::Deref,
};

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

impl FileSpecimen for TextSpecimen {}

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
