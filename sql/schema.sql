--
-- PostgreSQL database dump
--

\restrict Et49r1nSEPg3KemoRlnrXOCjirF6yWdduhKfNlkoyiY2nVbKlmHrQ1D5RyJhzKX

-- Dumped from database version 18.4 (Debian 18.4-1.pgdg13+1)
-- Dumped by pg_dump version 18.4 (Debian 18.4-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    customer_id character varying NOT NULL,
    customer_unique_id character varying NOT NULL,
    customer_zip_code_prefix character varying NOT NULL,
    customer_city character varying NOT NULL,
    customer_state character varying NOT NULL
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- Name: geolocation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.geolocation (
    geolocation_id bigint NOT NULL,
    geolocation_zip_code_prefix character varying NOT NULL,
    geolocation_lat numeric(10,8) NOT NULL,
    geolocation_lng numeric(11,8) NOT NULL,
    geolocation_city character varying NOT NULL,
    geolocation_state character varying NOT NULL
);


ALTER TABLE public.geolocation OWNER TO postgres;

--
-- Name: geolocation_geolocation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.geolocation_geolocation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.geolocation_geolocation_id_seq OWNER TO postgres;

--
-- Name: geolocation_geolocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.geolocation_geolocation_id_seq OWNED BY public.geolocation.geolocation_id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    order_id character varying NOT NULL,
    order_item_id integer NOT NULL,
    product_id character varying NOT NULL,
    seller_id character varying NOT NULL,
    shipping_limit_date timestamp without time zone NOT NULL,
    price numeric(10,2) NOT NULL,
    freight_value numeric(10,2) NOT NULL
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- Name: order_payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_payments (
    order_id character varying NOT NULL,
    payment_sequential integer NOT NULL,
    payment_type character varying NOT NULL,
    payment_installments integer NOT NULL,
    payment_value numeric(10,2) NOT NULL
);


ALTER TABLE public.order_payments OWNER TO postgres;

--
-- Name: order_reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_reviews (
    review_id character varying NOT NULL,
    order_id character varying NOT NULL,
    review_score integer NOT NULL,
    review_comment_title character varying,
    review_comment_message text,
    review_creation_date timestamp without time zone NOT NULL,
    review_answer_timestamp timestamp without time zone,
    review_pk bigint NOT NULL
);


ALTER TABLE public.order_reviews OWNER TO postgres;

--
-- Name: order_reviews_review_pk_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_reviews_review_pk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_reviews_review_pk_seq OWNER TO postgres;

--
-- Name: order_reviews_review_pk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_reviews_review_pk_seq OWNED BY public.order_reviews.review_pk;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    order_id character varying NOT NULL,
    customer_id character varying NOT NULL,
    order_status character varying NOT NULL,
    order_purchase_timestamp timestamp without time zone NOT NULL,
    order_approved_at timestamp without time zone,
    order_delivered_carrier_date timestamp without time zone,
    order_delivered_customer_date timestamp without time zone,
    order_estimated_delivery_date timestamp without time zone NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: product_category_translation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_category_translation (
    product_category_name character varying NOT NULL,
    product_category_name_english character varying
);


ALTER TABLE public.product_category_translation OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    product_id character varying NOT NULL,
    product_category_name character varying,
    product_name_lenght integer,
    product_description_lenght integer,
    product_photos_qty integer,
    product_weight_g integer,
    product_length_cm integer,
    product_height_cm integer,
    product_width_cm integer
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: sellers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sellers (
    seller_id character varying NOT NULL,
    seller_zip_code_prefix character varying NOT NULL,
    seller_city character varying NOT NULL,
    seller_state character varying NOT NULL
);


ALTER TABLE public.sellers OWNER TO postgres;

--
-- Name: geolocation geolocation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.geolocation ALTER COLUMN geolocation_id SET DEFAULT nextval('public.geolocation_geolocation_id_seq'::regclass);


--
-- Name: order_reviews review_pk; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_reviews ALTER COLUMN review_pk SET DEFAULT nextval('public.order_reviews_review_pk_seq'::regclass);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);


--
-- Name: geolocation geolocation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.geolocation
    ADD CONSTRAINT geolocation_pkey PRIMARY KEY (geolocation_id);


--
-- Name: order_reviews order_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_reviews
    ADD CONSTRAINT order_reviews_pkey PRIMARY KEY (review_pk);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: order_items pk_order_items; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT pk_order_items PRIMARY KEY (order_id, order_item_id);


--
-- Name: order_payments pk_order_payments; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_payments
    ADD CONSTRAINT pk_order_payments PRIMARY KEY (order_id, payment_sequential);


--
-- Name: product_category_translation product_category_translation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_category_translation
    ADD CONSTRAINT product_category_translation_pkey PRIMARY KEY (product_category_name);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: sellers sellers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sellers
    ADD CONSTRAINT sellers_pkey PRIMARY KEY (seller_id);


--
-- Name: orders fk_order_customer; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: order_items fk_order_items_order; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- Name: order_items fk_order_items_product; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: order_items fk_order_items_seller; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_order_items_seller FOREIGN KEY (seller_id) REFERENCES public.sellers(seller_id);


--
-- Name: order_payments fk_order_payments_order; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_payments
    ADD CONSTRAINT fk_order_payments_order FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- Name: order_reviews fk_review_order; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_reviews
    ADD CONSTRAINT fk_review_order FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- PostgreSQL database dump complete
--

\unrestrict Et49r1nSEPg3KemoRlnrXOCjirF6yWdduhKfNlkoyiY2nVbKlmHrQ1D5RyJhzKX

