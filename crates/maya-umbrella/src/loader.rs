use async_trait::async_trait;
use futures::future;

mod file_loader;

pub use file_loader::*;
#[async_trait]
pub trait Loader<T>
where
    T: Send,
    Self: Sized,
{
    type Error: Send;
    type Option: Sync + Send + ?Sized;

    async fn load(&self, option: &Self::Option) -> Result<T, Self::Error>;

    async fn multiple_load<P: AsRef<Self::Option> + Sync>(
        &self,
        options: &[P],
    ) -> Vec<Result<T, Self::Error>>
    where
        T: 'async_trait,
    {
        let results = future::join_all(
            options
                .iter()
                .map(|option| self.load(option.as_ref()))
                .collect::<Vec<_>>(),
        )
        .await;

        results
    }
}
