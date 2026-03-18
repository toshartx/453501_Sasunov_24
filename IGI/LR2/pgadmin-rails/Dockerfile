# Dockerfile
FROM ruby:3.2.0

# Устанавливаем зависимости
RUN apt-get update -qq && apt-get install -y \
    build-essential \
    libpq-dev \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем bundler
RUN gem install bundler

WORKDIR /app

# Копируем Gemfile и устанавливаем гемы
COPY Gemfile Gemfile.lock* ./
RUN bundle install --jobs 4 --retry 3

# Копируем приложение
COPY . .

# Исправляем права для Passenger
RUN chown -R root:root /usr/local/bundle && \
    chmod -R 755 /usr/local/bundle

EXPOSE 3000

# Запускаем через Passenger
CMD ["bundle", "exec", "passenger", "start", "--port", "3000", "--address", "0.0.0.0"]