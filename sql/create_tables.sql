--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Debian 15.1-1.pgdg110+1)
-- Dumped by pg_dump version 15.1

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
-- Name: depositewallets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.depositewallets (
    id integer NOT NULL,
    creation_time timestamp with time zone,
    address character varying,
    private_key bytea
);


ALTER TABLE public.depositewallets OWNER TO postgres;

--
-- Name: depositewallets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.depositewallets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.depositewallets_id_seq OWNER TO postgres;

--
-- Name: depositewallets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.depositewallets_id_seq OWNED BY public.depositewallets.id;


--
-- Name: deposits_transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.deposits_transactions (
    id integer NOT NULL,
    creation_time timestamp with time zone,
    amount numeric,
    currency character varying,
    to_address character varying,
    tx_id character varying,
    depositewallets_id integer
);


ALTER TABLE public.deposits_transactions OWNER TO postgres;

--
-- Name: deposits_transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.deposits_transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.deposits_transactions_id_seq OWNER TO postgres;

--
-- Name: deposits_transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.deposits_transactions_id_seq OWNED BY public.deposits_transactions.id;


--
-- Name: mainwallet_transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mainwallet_transaction (
    id integer NOT NULL,
    creation_time timestamp with time zone,
    amount numeric,
    currency character varying,
    to_address character varying,
    tx_id character varying
);


ALTER TABLE public.mainwallet_transaction OWNER TO postgres;

--
-- Name: mainwallet_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mainwallet_transaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mainwallet_transaction_id_seq OWNER TO postgres;

--
-- Name: mainwallet_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mainwallet_transaction_id_seq OWNED BY public.mainwallet_transaction.id;


--
-- Name: depositewallets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.depositewallets ALTER COLUMN id SET DEFAULT nextval('public.depositewallets_id_seq'::regclass);


--
-- Name: deposits_transactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deposits_transactions ALTER COLUMN id SET DEFAULT nextval('public.deposits_transactions_id_seq'::regclass);


--
-- Name: mainwallet_transaction id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mainwallet_transaction ALTER COLUMN id SET DEFAULT nextval('public.mainwallet_transaction_id_seq'::regclass);


--
-- Data for Name: depositewallets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.depositewallets (id, creation_time, address, private_key) FROM stdin;
1	2022-11-18 23:41:45.944434+00	0x7458b33Eab5a1d5B1E164063f35812ADAb0Ab8e0	\\x7363000218084302adbfa2cb117f590312b3acc991376489517f5c83da9fbef121bee884b6aeda9755eb6b1172d4d4adbebdea5ff96e3b7dbd9f1f198ffa0a11d50907c645b0b567f590da354f0712f4b4d2d07d3375b3bc8a270dc9ea602f3e7eeedcbf
2	2022-11-18 23:41:58.969888+00	0x970aEF9420F2a5E16eE8D77fad46cE3A37BD7372	\\x7363000212affa18c048aa5c23dcbf5683fe61e400564963c5233a84684df2f85cafdf8fded85cc4363f83a0562d20c82087bd0e7a1be6e8715c61a439c7ff030d5969d04cc9a47471ceed2ed31013e07f255c1cdaf6056f5dc3656065bdccf47ac390d2
3	2022-11-18 23:42:08.389135+00	0x57011eA40b994B9d2dD2359f766cB2D02AfD9B74	\\x73630002ed747def0417bc91257960348431eaca9243f3931b7e818bff6eca1124a3b23a74d3b0b98a7c2a753b5c913d541c8a7709195abb93bceecee2d874368f79fedf12afec2075767949d15e304831b9c346d28352d7a82fd8bacb8eb1684c7e84de
5	2022-11-19 01:04:05.290489+00	0x103560C89f89e56773B921510402c79ca701555a	\\x73630002fb51e386efc2e4a55f3a75762c965a8ec045dc274d112caa08a7a980779848d4c70960725aa96f873622007b080ede473918e771a160d08bb0c3f3cdbffa4247be6d51be245422dc3c41de1ad096176ee8b8f57c765f31494de2a17039596199
6	2022-11-20 19:42:15.57233+00	0xC3E5AdCF1fd38192ca5674eA2742A7d275BF4Dd9	\\x736300021de8e5401453020066aa527c1d829e3134fe5d6aa8abaf7f3023ca731b056a2d7190f845a276c569bc9a1f83e61b7b5e8e7d368109cb15e8e3cd34f84fafe5ce31f06c4a978f3e8b2387e65ff78e6384e98908e188638c2a2151275698c55b42
39	2022-11-20 20:39:27.612681+00	0x5c728B008c0f45bC9E188C3A676217183B23Af48	\\x73630002d4d61b7853763220aecd5898c1671160a351fea7c98a1dac79ac18af866b7eef91ac8cf1a5ffa1761dbb4be701b6c5124e3baf96cb36fa27c68ce4fccbfd027054df43344ac36cfa72e613f31c5f8c646afeac4517ebd907dd1e85eede22ae41
\.


--
-- Data for Name: deposits_transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.deposits_transactions (id, creation_time, amount, currency, to_address, tx_id, depositewallets_id) FROM stdin;
1	2022-11-19 17:32:11.219676+00	0.5	USDT	0x51a6505c7DE0a718094ABC33aaB758D011C24522	0xf1a68e6ebdde18737d321f1897be7e4bdb8635798653af3e89bc8a64708200f5	5
2	2022-11-19 17:32:11.219676+00	0.4	BNBT	0x970aEF9420F2a5E16eE8D77fad46cE3A37BD7372	0xc50257bba36a9813460bee9bc0d1346046129ac5dcc61e3ac010a25bf92b965d	5
3	2022-11-20 09:29:49.247694+00	0.04979	BNBT	0x51a6505c7DE0a718094ABC33aaB758D011C24522	0x821c072b0d9312bb581251e46f0190dd3a230c60f29c59121a958f1dc36d1818	1
4	2022-11-20 09:29:49.247694+00	0.39979	BNBT	0x51a6505c7DE0a718094ABC33aaB758D011C24522	0xed1770356feb1f1f6845e71a79446e2a38bf693b09af76df10367e1fef192b15	2
5	2022-11-20 09:29:49.247694+00	0.09921897	BNBT	0x51a6505c7DE0a718094ABC33aaB758D011C24522	0x1283940c59e9f72e598a8caf566d8dedeca38054070bc85b66d105512446289b	5
6	2022-11-20 10:02:03.645885+00	0.09979	BNBT	0x51a6505c7DE0a718094ABC33aaB758D011C24522	0x9f94d107b2b5c058def0b9c5e2cfa192e0db2b00429b9780111e289231b3177b	1
7	2022-11-20 10:02:03.645885+00	0.09979	BNBT	0x51a6505c7DE0a718094ABC33aaB758D011C24522	0x7bfe4f737833b24f15b1e7593efc8fb113672f9a831e3fe8c107c3a795135692	2
8	2022-11-20 10:02:03.645885+00	0.7058	USDT	0x51a6505c7DE0a718094ABC33aaB758D011C24522	0xb9ecb4203ac6e20863e674ef7fa6b6b4b68ebe80b152d17ad30a320e6e4e5994	3
9	2022-11-20 10:02:03.645885+00	0.19942885	BNBT	0x51a6505c7DE0a718094ABC33aaB758D011C24522	0x7eb794d9c79e7b3fa86a6ef221d64d9469e2528efaaf78c1ab3d2a08679a64cf	3
10	2022-11-20 10:02:03.645885+00	0.9958	USDT	0x51a6505c7DE0a718094ABC33aaB758D011C24522	0x6fa58150fd0838a8b743bbb899ca749732fcee93960c9365ce23b2744ed2fd0f	5
11	2022-11-20 10:02:03.645885+00	0.19942885	BNBT	0x51a6505c7DE0a718094ABC33aaB758D011C24522	0xfc6895ad3849638f9bd98b67d52768f6039aa14197686eb2e6d118179f01e06c	5
\.


--
-- Data for Name: mainwallet_transaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mainwallet_transaction (id, creation_time, amount, currency, to_address, tx_id) FROM stdin;
1	2022-11-18 23:43:11.488835+00	0.5	USDT	0x57011eA40b994B9d2dD2359f766cB2D02AfD9B74	0x025d23da027896fc8c281c1d7b7302a7575807ee34bee3d66edcfa1d40481525
2	2022-11-19 00:02:41.571112+00	0.1	USDT	0x57011eA40b994B9d2dD2359f766cB2D02AfD9B74	0x09916b0ca37d49aa88e4950f9b3d6e6f7a37bf099bc3ac941ff4daf174f89a07
3	2022-11-19 00:31:20.438168+00	0.1	USDT	0x57011eA40b994B9d2dD2359f766cB2D02AfD9B74	0xf5ce17694af5b8412afd8cb943dd4aba1536b4b8a58abae981fe2465d12b3d02
4	2022-11-19 00:33:23.224923+00	0.01	USDT	0x57011eA40b994B9d2dD2359f766cB2D02AfD9B74	0x37212a25b564ca81f31709504496560ef39050ffe06fa6d6364b4c435d87b6f5
5	2022-11-19 01:07:57.387132+00	1	USDT	0x103560C89f89e56773B921510402c79ca701555a	0x5ed2ccf4ed0268ec825f8ebe13fcc294d628f30fe77af44774c1d72a71607cd2
6	2022-11-19 17:32:11.214335+00	0.5	USDT	0x103560C89f89e56773B921510402c79ca701555a	0x69f72521e2e9d43c3b3a87267b7a22c5d2a3766eb3da56d0291e865de3f6bbca
7	2022-11-19 17:32:11.214335+00	0.05	BNBT	0x7458b33Eab5a1d5B1E164063f35812ADAb0Ab8e0	0xc705fa01d027b21be0b23abe0d2665b67007b4f1e35cbdbe1aa169c72f45a589
8	2022-11-20 09:50:20.063442+00	0.2	BNBT	0x103560C89f89e56773B921510402c79ca701555a	0x19a95bf99344fa042ef9aa3e6cdb856bca7de64c5019fce80ce1aada36a4fd4d
9	2022-11-20 09:50:20.063442+00	0.2	BNBT	0x57011eA40b994B9d2dD2359f766cB2D02AfD9B74	0xa91bcf1383388d7d5668ea8f368542fb2803c4652d9cd288c77a6a48a5fc6c29
10	2022-11-20 09:50:20.063442+00	0.1	BNBT	0x7458b33Eab5a1d5B1E164063f35812ADAb0Ab8e0	0x4d1d524ec410ce7bbcdcbecc850573fe8965a3fae4f7846e4ce2ef57f6a15c05
11	2022-11-20 09:50:20.063442+00	0.1	BNBT	0x970aEF9420F2a5E16eE8D77fad46cE3A37BD7372	0xf07c2c876b2f39085993d8f1cb8457dbf6b3b80e8e20be44e4fc7304082423ca
12	2022-11-20 20:39:27.609473+00	0.1	BNBT	0x970aEF9420F2a5E16eE8D77fad46cE3A37BD7372	0x80e32260c85c66334afcd3aef7f4a5c50b84f9a31fd5718609eab1467bd865cb
\.


--
-- Name: depositewallets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.depositewallets_id_seq', 39, true);


--
-- Name: deposits_transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.deposits_transactions_id_seq', 11, true);


--
-- Name: mainwallet_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mainwallet_transaction_id_seq', 12, true);


--
-- Name: depositewallets depositewallets_address_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.depositewallets
    ADD CONSTRAINT depositewallets_address_key UNIQUE (address);


--
-- Name: depositewallets depositewallets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.depositewallets
    ADD CONSTRAINT depositewallets_pkey PRIMARY KEY (id);


--
-- Name: deposits_transactions deposits_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deposits_transactions
    ADD CONSTRAINT deposits_transactions_pkey PRIMARY KEY (id);


--
-- Name: mainwallet_transaction mainwallet_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mainwallet_transaction
    ADD CONSTRAINT mainwallet_transaction_pkey PRIMARY KEY (id);


--
-- Name: ix_depositewallets_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_depositewallets_id ON public.depositewallets USING btree (id);


--
-- Name: ix_deposits_transactions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_deposits_transactions_id ON public.deposits_transactions USING btree (id);


--
-- Name: ix_mainwallet_transaction_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_mainwallet_transaction_id ON public.mainwallet_transaction USING btree (id);


--
-- Name: deposits_transactions deposits_transactions_depositewallets_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deposits_transactions
    ADD CONSTRAINT deposits_transactions_depositewallets_id_fkey FOREIGN KEY (depositewallets_id) REFERENCES public.depositewallets(id);


--
-- PostgreSQL database dump complete
--

