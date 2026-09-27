# petit -- log analysis for systems administrators
# Built on Hummingbird Python images (Red Hat UBI-based).
#
# Pure stdlib, no runtime dependencies, so the runtime stage needs nothing
# beyond the venv itself.
#
# Build:
#   podman build -f Containerfile -t petit:local .
#
# Run:
#   podman run --rm -v $(pwd):/data:ro,Z petit:local --hash /data/some.log

# Stage 1: Builder (has shell, dnf, build tools)
FROM quay.io/hummingbird/python:latest-fips-builder AS builder
USER 0
WORKDIR /app
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY pyproject.toml README.md COPYING CHANGELOG.md AUTHORS ./
COPY src/ ./src/
RUN pip install --no-cache-dir .

# Stage 2: Runtime (distroless -- no shell, no package manager)
FROM quay.io/hummingbird/python:latest-fips
COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

LABEL name="petit" \
      version="4.8.0" \
      summary="Log analysis for systems administrators" \
      description="Detects the log format, then collapses the repetitive into counts so the unusual is what you read" \
      maintainer="crunchtools.com" \
      org.opencontainers.image.source="https://github.com/crunchtools/petit" \
      org.opencontainers.image.description="Log analysis for systems administrators" \
      org.opencontainers.image.licenses="AGPL-3.0-or-later"

ENTRYPOINT ["petit"]
