-- +goose Up
-- +goose StatementBegin
CREATE TABLE t_healthcheck (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,
  name VARCHAR(255) NOT NULL,
  status BOOLEAN NOT NULL,
  message TEXT
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE t_healthcheck;
-- +goose StatementEnd
