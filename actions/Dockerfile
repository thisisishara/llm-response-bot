FROM rasa/rasa-sdk:3.6.1@sha256:492503069f8e74e760673f325dd4537d2cf355b1f2b4123d55687f285ad6aa88

# Change back to root user to install dependencies
USER root

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY .. /app/actions/

USER 1001
CMD ["start", "--actions", "actions"]