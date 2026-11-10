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

# Stage 0: Lock (resolve pinned deps from the committed uv.lock, not a fresh
# resolve -- see RT#1564)
FROM quay.io/hummingbird/python:3.14-fips-builder AS lock
USER 0
RUN pip install --no-cache-dir uv==0.13.7
WORKDIR /lock
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --no-emit-project \
      --format requirements-txt -o /requirements.txt

# Stage 1: Builder (has shell, dnf, build tools)
FROM quay.io/hummingbird/python:3.14-fips-builder AS builder
USER 0
WORKDIR /app
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY --from=lock /requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --no-deps -r /tmp/requirements.txt
COPY pyproject.toml README.md COPYING CHANGELOG.md AUTHORS ./
COPY src/ ./src/
RUN pip install --no-cache-dir --no-deps .

# Stage 2: Runtime (distroless -- no shell, no package manager)
FROM quay.io/hummingbird/python:3.14-fips
COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

LABEL name="petit" \
      version="4.10.3" \
      summary="Log analysis for systems administrators" \
      description="Detects the log format, then collapses the repetitive into counts so the unusual is what you read" \
      maintainer="crunchtools.com" \
      org.opencontainers.image.source="https://github.com/crunchtools/petit" \
      org.opencontainers.image.description="Log analysis for systems administrators" \
      org.opencontainers.image.licenses="AGPL-3.0-or-later"

ENTRYPOINT ["petit"]
