# Pull base image
FROM helsinkitest/python-node:3.6-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install packages
RUN apt-get update \
   && apt-get install --no-install-recommends -y \
    jpeg-dev \
    gettext \ 
    build-essential \
    git \
    libxslt-dev \
    zlib-dev \
    libpq-dev 

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN git config --global http.postBuffer 524288000 \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt --src /usr/local/src \
    && npm install \
    # && yarn cache clean \
	&& npm install -g coffee-script@^1.12.6
	&& apt-get remove -y build-essential \
	&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf /var/cache/apt/archives 

COPY package.json .
RUN npm install
RUN npm install -g coffee-script@^1.12.6

# Copy project
COPY . /code/

# Entrypoint
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
