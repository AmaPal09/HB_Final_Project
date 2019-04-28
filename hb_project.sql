--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6 (Ubuntu 10.6-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.6 (Ubuntu 10.6-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: agencies; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.agencies (
    agency_id integer NOT NULL,
    agency_tag character varying(20) NOT NULL,
    agency_short_title character varying(30) NOT NULL,
    agency_title character varying(50) NOT NULL,
    region_id integer
);


ALTER TABLE public.agencies OWNER TO vagrant;

--
-- Name: agencies_agency_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.agencies_agency_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.agencies_agency_id_seq OWNER TO vagrant;

--
-- Name: agencies_agency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.agencies_agency_id_seq OWNED BY public.agencies.agency_id;


--
-- Name: bus_route; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.bus_route (
    bus_route_id integer NOT NULL,
    title character varying(50) NOT NULL,
    tag character varying(20) NOT NULL,
    route_id integer,
    direction_id integer,
    stop_id integer
);


ALTER TABLE public.bus_route OWNER TO vagrant;

--
-- Name: bus_route_bus_route_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.bus_route_bus_route_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bus_route_bus_route_id_seq OWNER TO vagrant;

--
-- Name: bus_route_bus_route_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.bus_route_bus_route_id_seq OWNED BY public.bus_route.bus_route_id;


--
-- Name: directions; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.directions (
    direction_id integer NOT NULL,
    direction character varying(15) NOT NULL
);


ALTER TABLE public.directions OWNER TO vagrant;

--
-- Name: directions_direction_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.directions_direction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.directions_direction_id_seq OWNER TO vagrant;

--
-- Name: directions_direction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.directions_direction_id_seq OWNED BY public.directions.direction_id;


--
-- Name: ratings; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.ratings (
    rating_id integer NOT NULL,
    rating_datetime timestamp without time zone NOT NULL,
    crowd_rating integer,
    time_rating integer,
    cleanliness_rating integer,
    safety_rating integer,
    outer_view_rating integer,
    rating_text integer
);


ALTER TABLE public.ratings OWNER TO vagrant;

--
-- Name: ratings_rating_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.ratings_rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ratings_rating_id_seq OWNER TO vagrant;

--
-- Name: ratings_rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.ratings_rating_id_seq OWNED BY public.ratings.rating_id;


--
-- Name: regions; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.regions (
    region_id integer NOT NULL,
    region character varying(50) NOT NULL
);


ALTER TABLE public.regions OWNER TO vagrant;

--
-- Name: regions_region_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.regions_region_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.regions_region_id_seq OWNER TO vagrant;

--
-- Name: regions_region_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.regions_region_id_seq OWNED BY public.regions.region_id;


--
-- Name: routes; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.routes (
    route_id integer NOT NULL,
    agency_id integer,
    route_tag character varying(10) NOT NULL,
    route_title character varying(50) NOT NULL
);


ALTER TABLE public.routes OWNER TO vagrant;

--
-- Name: routes_route_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.routes_route_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.routes_route_id_seq OWNER TO vagrant;

--
-- Name: routes_route_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.routes_route_id_seq OWNED BY public.routes.route_id;


--
-- Name: stops; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.stops (
    stop_id integer NOT NULL,
    stop_tag character varying(6) NOT NULL,
    stop_id_tag character varying(10) NOT NULL,
    stop_title character varying(30) NOT NULL,
    stop_lon double precision NOT NULL,
    stop_lat double precision NOT NULL
);


ALTER TABLE public.stops OWNER TO vagrant;

--
-- Name: stops_stop_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.stops_stop_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stops_stop_id_seq OWNER TO vagrant;

--
-- Name: stops_stop_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.stops_stop_id_seq OWNED BY public.stops.stop_id;


--
-- Name: user_ratings; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.user_ratings (
    user_id integer,
    rating_id integer,
    bus_route_id integer,
    trip_datetime timestamp without time zone NOT NULL
);


ALTER TABLE public.user_ratings OWNER TO vagrant;

--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_fname character varying(30) NOT NULL,
    user_lname character varying(30) NOT NULL,
    user_email character varying(60) NOT NULL,
    user_pwd character varying(30) NOT NULL
);


ALTER TABLE public.users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: agencies agency_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.agencies ALTER COLUMN agency_id SET DEFAULT nextval('public.agencies_agency_id_seq'::regclass);


--
-- Name: bus_route bus_route_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.bus_route ALTER COLUMN bus_route_id SET DEFAULT nextval('public.bus_route_bus_route_id_seq'::regclass);


--
-- Name: directions direction_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.directions ALTER COLUMN direction_id SET DEFAULT nextval('public.directions_direction_id_seq'::regclass);


--
-- Name: ratings rating_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.ratings ALTER COLUMN rating_id SET DEFAULT nextval('public.ratings_rating_id_seq'::regclass);


--
-- Name: regions region_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.regions ALTER COLUMN region_id SET DEFAULT nextval('public.regions_region_id_seq'::regclass);


--
-- Name: routes route_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.routes ALTER COLUMN route_id SET DEFAULT nextval('public.routes_route_id_seq'::regclass);


--
-- Name: stops stop_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.stops ALTER COLUMN stop_id SET DEFAULT nextval('public.stops_stop_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: agencies; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.agencies (agency_id, agency_tag, agency_short_title, agency_title, region_id) FROM stdin;
\.


--
-- Data for Name: bus_route; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.bus_route (bus_route_id, title, tag, route_id, direction_id, stop_id) FROM stdin;
\.


--
-- Data for Name: directions; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.directions (direction_id, direction) FROM stdin;
\.


--
-- Data for Name: ratings; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.ratings (rating_id, rating_datetime, crowd_rating, time_rating, cleanliness_rating, safety_rating, outer_view_rating, rating_text) FROM stdin;
\.


--
-- Data for Name: regions; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.regions (region_id, region) FROM stdin;
\.


--
-- Data for Name: routes; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.routes (route_id, agency_id, route_tag, route_title) FROM stdin;
\.


--
-- Data for Name: stops; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.stops (stop_id, stop_tag, stop_id_tag, stop_title, stop_lon, stop_lat) FROM stdin;
\.


--
-- Data for Name: user_ratings; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.user_ratings (user_id, rating_id, bus_route_id, trip_datetime) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.users (user_id, user_fname, user_lname, user_email, user_pwd) FROM stdin;
\.


--
-- Name: agencies_agency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.agencies_agency_id_seq', 1, false);


--
-- Name: bus_route_bus_route_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.bus_route_bus_route_id_seq', 1, false);


--
-- Name: directions_direction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.directions_direction_id_seq', 1, false);


--
-- Name: ratings_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.ratings_rating_id_seq', 1, false);


--
-- Name: regions_region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.regions_region_id_seq', 1, false);


--
-- Name: routes_route_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.routes_route_id_seq', 1, false);


--
-- Name: stops_stop_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.stops_stop_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: agencies agencies_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.agencies
    ADD CONSTRAINT agencies_pkey PRIMARY KEY (agency_id);


--
-- Name: bus_route bus_route_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.bus_route
    ADD CONSTRAINT bus_route_pkey PRIMARY KEY (bus_route_id);


--
-- Name: directions directions_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.directions
    ADD CONSTRAINT directions_pkey PRIMARY KEY (direction_id);


--
-- Name: ratings ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (rating_id);


--
-- Name: regions regions_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.regions
    ADD CONSTRAINT regions_pkey PRIMARY KEY (region_id);


--
-- Name: routes routes_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_pkey PRIMARY KEY (route_id);


--
-- Name: stops stops_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.stops
    ADD CONSTRAINT stops_pkey PRIMARY KEY (stop_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: agencies agencies_region_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.agencies
    ADD CONSTRAINT agencies_region_id_fkey FOREIGN KEY (region_id) REFERENCES public.regions(region_id);


--
-- Name: bus_route bus_route_direction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.bus_route
    ADD CONSTRAINT bus_route_direction_id_fkey FOREIGN KEY (direction_id) REFERENCES public.directions(direction_id);


--
-- Name: bus_route bus_route_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.bus_route
    ADD CONSTRAINT bus_route_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(route_id);


--
-- Name: bus_route bus_route_stop_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.bus_route
    ADD CONSTRAINT bus_route_stop_id_fkey FOREIGN KEY (stop_id) REFERENCES public.stops(stop_id);


--
-- Name: routes routes_agency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_agency_id_fkey FOREIGN KEY (agency_id) REFERENCES public.agencies(agency_id);


--
-- Name: user_ratings user_ratings_bus_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_ratings
    ADD CONSTRAINT user_ratings_bus_route_id_fkey FOREIGN KEY (bus_route_id) REFERENCES public.bus_route(bus_route_id);


--
-- Name: user_ratings user_ratings_rating_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_ratings
    ADD CONSTRAINT user_ratings_rating_id_fkey FOREIGN KEY (rating_id) REFERENCES public.ratings(rating_id);


--
-- Name: user_ratings user_ratings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_ratings
    ADD CONSTRAINT user_ratings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

