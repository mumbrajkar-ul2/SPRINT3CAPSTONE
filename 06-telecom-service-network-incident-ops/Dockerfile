# Runs the test suite in a clean Linux container with the same Python as CI.
#
#   docker build -t telecom-ops-tests .
#   docker run --rm telecom-ops-tests
#
# Stage S04-05 Half B. PROPOSED. Owner: Team-Force.
# The tag 3.11-slim moves. The image digest seen on 2026-10-11 was
# sha256:e88e9763f943ec1834f992a4b51e0f24500486803e8bc534e5767af9ea65f6ce

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install packages first so this layer is reused when only source files change.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# The tests write logs/audit.log, so the run user owns /app.
RUN useradd --create-home app && chown -R app:app /app
USER app

CMD ["python", "-m", "pytest", "-q"]
