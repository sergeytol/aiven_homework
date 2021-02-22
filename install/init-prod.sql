--
-- PostgreSQL database dump
--

-- Dumped from database version 12.6
-- Dumped by pg_dump version 12.6 (Debian 12.6-1.pgdg100+1)

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

SET default_table_access_method = heap;

--
-- Name: website_check_result; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.website_check_result (
    id bigint NOT NULL,
    url text NOT NULL,
    successful boolean,
    status_code smallint,
    request_time real,
    pattern_match boolean,
    checked_at timestamp with time zone NOT NULL,
    received_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    error_message text
);


ALTER TABLE public.website_check_result OWNER TO avnadmin;

--
-- Name: website_check_result_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.website_check_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.website_check_result_id_seq OWNER TO avnadmin;

--
-- Name: website_check_result_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.website_check_result_id_seq OWNED BY public.website_check_result.id;


--
-- Name: website_check_result_status_code_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.website_check_result_status_code_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.website_check_result_status_code_seq OWNER TO avnadmin;

--
-- Name: website_check_result_status_code_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.website_check_result_status_code_seq OWNED BY public.website_check_result.status_code;


--
-- Name: website_check_result id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.website_check_result ALTER COLUMN id SET DEFAULT nextval('public.website_check_result_id_seq'::regclass);


--
-- Name: website_check_result status_code; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.website_check_result ALTER COLUMN status_code SET DEFAULT nextval('public.website_check_result_status_code_seq'::regclass);


--
-- PostgreSQL database dump complete
--
