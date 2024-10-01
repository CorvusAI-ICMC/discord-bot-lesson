FROM mambaorg/micromamba:bookworm-slim AS base

COPY env.yml /tmp/env.yml
RUN micromamba install -c conda-forge -y -n base -f /tmp/env.yml && micromamba clean --all --yes

FROM base AS runner

# The package name wher the soure is located
ARG PACKAGE_NAME=demo_bot
ENV PACKAGE_NAME=${PACKAGE_NAME}

# Create app directory
USER root
RUN mkdir /app && chown $MAMBA_USER:$MAMBA_USER /app

# Scale down privileges
USER $MAMBA_USER
WORKDIR /app
COPY --chown=$MAMBA_USER:$MAMBA_USER ./${PACKAGE_NAME} /app/${PACKAGE_NAME}

# ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]
# CMD ["/bin/bash", "-c", "micromamba run -n base python"]

CMD [ "/bin/bash", "-c", "python ./${PACKAGE_NAME}" ]



