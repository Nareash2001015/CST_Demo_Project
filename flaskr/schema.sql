DROP TABLE IF EXISTS cst_info;

CREATE TABLE cst_info (
    id SERIAL PRIMARY KEY,
    customer_key VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_base_version VARCHAR(50) NOT NULL,
    update_level INT NOT NULL,
);

INSERT INTO cst_info (customer_key, product_name, product_base_version, update_level, project_key) VALUES
    ('BNYM', 'wso2am', '3.2.0', 66, 'ABC123'),
    ('Credit Agricole', 'wso2am', '3.2.0', 66, 'ABC123'),
    ('Credit Agricole', 'choreo-connect', '2.5', 26, 'DEF456'),
    ('BNYM', 'wso2am', '4.2.0', 24, 'GHI789'),
    ('BNYM', 'wso2ei', '1.8', 18, 'JKL012'),
    ('Credit Agricole', 'wso2esb', '4.1', 23, 'MNO345');