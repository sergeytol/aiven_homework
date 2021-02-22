--
-- PostgreSQL database dump
--

-- Dumped from database version 11.3 (Debian 11.3-1.pgdg90+1)
-- Dumped by pg_dump version 11.3 (Debian 11.3-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: website_check_result; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.website_check_result (
    id bigint NOT NULL,
    url text NOT NULL,
    successful boolean,
    status_code smallint NULL,
    request_time real,
    pattern_match boolean,
    checked_at timestamp with time zone NOT NULL,
    received_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    error_message text
);


ALTER TABLE public.website_check_result OWNER TO postgres;

--
-- Name: website_check_result_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.website_check_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.website_check_result_id_seq OWNER TO postgres;

--
-- Name: website_check_result_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.website_check_result_id_seq OWNED BY public.website_check_result.id;


--
-- Name: website_check_result_status_code_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.website_check_result_status_code_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.website_check_result_status_code_seq OWNER TO postgres;

--
-- Name: website_check_result_status_code_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.website_check_result_status_code_seq OWNED BY public.website_check_result.status_code;


--
-- Name: website_check_result id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.website_check_result ALTER COLUMN id SET DEFAULT nextval('public.website_check_result_id_seq'::regclass);


--
-- Name: website_check_result status_code; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.website_check_result ALTER COLUMN status_code SET DEFAULT nextval('public.website_check_result_status_code_seq'::regclass);


--
-- Data for Name: website_check_result; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.website_check_result (id, url, successful, status_code, request_time, pattern_match, checked_at, received_at, error_message) FROM stdin;
\.


--
-- Name: website_check_result_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.website_check_result_id_seq', 1, false);


--
-- Name: website_check_result_status_code_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.website_check_result_status_code_seq', 1, false);


--
-- Name: website_check_result website_check_result_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.website_check_result
    ADD CONSTRAINT website_check_result_pk PRIMARY KEY (id);


--
-- Name: website_check_result_checked_at_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX website_check_result_checked_at_index ON public.website_check_result USING btree (checked_at DESC);


--
-- Name: website_check_result_received_at_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX website_check_result_received_at_index ON public.website_check_result USING btree (received_at DESC);


--
-- Name: website_check_result_status_code_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX website_check_result_status_code_index ON public.website_check_result USING btree (status_code);


--
-- Name: website_check_result_url_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX website_check_result_url_index ON public.website_check_result USING btree (url);


--
-- PostgreSQL database dump complete
--

