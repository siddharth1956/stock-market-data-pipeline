
CREATE TABLE exchange (
    exchange_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exchange_name VARCHAR(50) NOT NULL,
    timezone VARCHAR(50)
);

CREATE TABLE stock (
    stock_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    exchange_id INTEGER,
    CONSTRAINT fk_exchange
        FOREIGN KEY (exchange_id)
        REFERENCES exchange(exchange_id)
);


CREATE TABLE daily_price (
    price_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    stock_id INTEGER NOT NULL,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10,2),
    high_price DECIMAL(10,2),
    low_price DECIMAL(10,2),
    close_price DECIMAL(10,2),
    volume BIGINT,
    CONSTRAINT fk_stock
        FOREIGN KEY (stock_id)
        REFERENCES stock(stock_id),
    CONSTRAINT uq_stock_date
        UNIQUE (stock_id, trade_date)
);