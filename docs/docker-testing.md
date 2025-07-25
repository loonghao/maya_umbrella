# Docker Integration Testing for Maya Umbrella

This document describes the Docker-based integration tests that run automatically in CI environments.

## Overview

Maya Umbrella includes Docker-based integration tests that run in real Maya environments using the [mottosso/maya](https://github.com/mottosso/docker-maya) Docker images. These tests are **automatically skipped locally** and only run in CI environments like GitHub Actions.

## Local Development

**Docker tests are automatically skipped during local development** - you don't need Docker installed locally. The tests will show as "skipped" in pytest output:

```bash
# Normal local testing (Docker tests skipped automatically)
nox -s pytest
# or
pytest

# Output will show:
# ========================== 58 passed, 8 skipped in 1.25s ==========================
```

## CI-Only Testing

Docker tests are designed to run only in CI environments. They are automatically skipped locally unless you explicitly force them to run.

### Force Running Docker Tests Locally (Optional)

If you need to run Docker tests locally for debugging:

```bash
# Prerequisites: Docker installed and running
# 1. Pull Maya Docker image
docker pull mottosso/maya:2022

# 2. Force run Docker tests (bypasses CI check)
CI=1 pytest tests/test_docker_integration.py -v -m docker

# 3. Or use nox with CI environment variable
CI=1 nox -s docker-test
```

### Normal CI Workflow

In CI environments (GitHub Actions, Travis, etc.), Docker tests run automatically:

```bash
# CI automatically runs these tests
pytest tests/test_docker_integration.py -v -m docker
```

## Test Categories

### Integration Tests (`@pytest.mark.docker`)

These tests run in real Maya environments and test:

1. **Basic Import Tests**: Verify Maya Umbrella imports correctly
2. **Defender Tests**: Test virus detection in clean and infected scenes
3. **Scanner Tests**: Test file scanning functionality
4. **Vaccine Tests**: Test vaccine application
5. **Version Compatibility**: Test across different Maya versions

### Test Structure

```python
@pytest.mark.docker
@pytest.mark.integration
class TestDockerMayaIntegration:
    def test_docker_maya_basic_import(self, docker_maya_runner):
        # Test basic functionality
        pass
```

## Available Docker Images

| Maya Version | Docker Image | Status |
|--------------|--------------|--------|
| 2022 | `mottosso/maya:2022` | ✅ Stable |
| 2023 | `mottosso/maya:2023` | ⚠️ Beta |
| 2024 | `mottosso/maya:2024` | ⚠️ Beta |

## Configuration

### Environment Variables

- `PYTHONPATH=/workspace`: Ensures Maya Umbrella is importable
- `MAYA_DISABLE_CIP=1`: Disables Customer Improvement Program
- `MAYA_DISABLE_CER=1`: Disables Customer Error Reporting

### Docker Compose

Use the provided `docker-compose.test.yml` for more complex testing scenarios:

```bash
# Start Maya 2022 container
docker-compose -f docker-compose.test.yml up maya-test

# Start Maya 2023 container (if available)
docker-compose -f docker-compose.test.yml --profile maya2023 up maya-2023-test
```

## CI/CD Integration

### GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/docker-integration-test.yml`) that:

1. Runs on push/PR to main branches
2. Tests with Maya 2022 by default
3. Optionally tests with Maya 2023/2024 on manual trigger
4. Uploads test results as artifacts

### Running in CI

```yaml
- name: Run Docker integration tests
  run: |
    docker run --rm \
      -v ${{ github.workspace }}:/workspace \
      -w /workspace \
      -e PYTHONPATH=/workspace \
      mottosso/maya:2022 \
      python -m pytest tests/test_docker_integration.py -v -m docker
```

## Troubleshooting

### Common Issues

1. **Docker not available**
   ```bash
   # Check Docker status
   docker --version
   docker info
   ```

2. **Maya image not found**
   ```bash
   # Pull the image manually
   docker pull mottosso/maya:2022
   ```

3. **Permission issues**
   ```bash
   # Fix file permissions
   chmod -R 755 .
   ```

4. **Memory issues**
   ```bash
   # Increase Docker memory limit (Docker Desktop)
   # Recommended: 4GB+ for Maya containers
   ```

### Debug Mode

Run tests with verbose output:

```bash
python scripts/docker_test_setup.py --run-tests --maya-version 2022
```

### Manual Testing

For manual testing and debugging:

```bash
# Start interactive container
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  -e PYTHONPATH=/workspace \
  mottosso/maya:2022 \
  bash

# Inside container, run Maya
mayapy
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Resource Cleanup**: Always clean up Maya scenes between tests
3. **Timeout Handling**: Set appropriate timeouts for Docker operations
4. **Image Management**: Regularly update Maya Docker images
5. **Mock vs Real**: Use Docker tests for integration, mocks for unit tests

## Performance Considerations

- Docker tests are slower than unit tests
- Maya startup time: ~10-30 seconds per container
- Image size: ~2-4GB per Maya version
- Recommended for CI: Maya 2022 only
- Recommended for development: All versions

## Contributing

When adding new Docker tests:

1. Mark tests with `@pytest.mark.docker`
2. Use the `docker_maya_runner` fixture
3. Include proper error handling
4. Test with multiple Maya versions when possible
5. Update this documentation
