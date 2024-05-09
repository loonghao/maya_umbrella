use cpython::py_module_initializer;

py_module_initializer!(maya_umbrella_rs, |py, m| {
    m.add(py, "__doc__", "Maya Umbrella API powered by Rust language")?;
    Ok(())
});
