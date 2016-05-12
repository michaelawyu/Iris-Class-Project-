CREATE TABLE USERS (
	user_id SERIAL PRIMARY KEY,
	username text NOT NULL UNIQUE,
	password text,
	if_dev boolean,
	if_firstrun boolean);

CREATE TABLE DEVS_PRODUCTS (
	user_id SERIAL PRIMARY KEY,
	product_id SERIAL NOT NULL UNIQUE,
	product_name text,
	if_upvote_allowed boolean,
	if_downvote_allowed boolean,
	max_votes int,
	if_followup_allowed boolean,
	if_user_generated_feature_request_allowed boolean,
	FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE);

CREATE TABLE SIGNUP (
	user_id SERIAL PRIMARY KEY,
	product_id SERIAL,
	votes_left int,
	FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE,
	FOREIGN KEY (product_id) REFERENCES DEVS_PRODUCTS(product_id) ON DELETE CASCADE);

CREATE TABLE SECTIONS_NEW (
	section_id SERIAL,
	product_id SERIAL,
	section_name text,
	PRIMARY KEY (product_id, section_id),
	FOREIGN KEY (product_id) REFERENCES DEVS_PRODUCTS(product_id) ON DELETE CASCADE);

CREATE TABLE POSTS_NEW (
	post_id SERIAL,
	section_id SERIAL,
	product_id SERIAL,
	post_title text,
	post_content text,
	upvotes int,
	downvotes int,
	if_dev_generated_feature_request boolean,
	PRIMARY KEY (product_id, section_id, post_id),
	FOREIGN KEY (product_id, section_id) REFERENCES SECTIONS_NEW(product_id, section_id) ON DELETE CASCADE);

CREATE TABLE FOLLOWUPS_NEW (
	followup_id SERIAL,
	post_id SERIAL,
	section_id SERIAL,
	product_id SERIAL,
	followup_content text,
	PRIMARY KEY (product_id, section_id, post_id, followup_id),
	FOREIGN KEY (product_id, section_id, post_id) REFERENCES POSTS_NEW(product_id, section_id, post_id) ON DELETE CASCADE);

CREATE TABLE USERS_POSTS_NEW (
	user_id SERIAL,
	username text,
	post_id SERIAL,
	post_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (user_id, post_id),
	FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE,
	FOREIGN KEY (username) REFERENCES USERS(username) ON DELETE CASCADE);

CREATE TABLE USERS_VOTES_NEW (
	user_id SERIAL,
	post_id SERIAL,
	if_upvoted boolean,
	if_downvoted boolean,
	PRIMARY KEY (user_id, post_id));

CREATE TABLE USERS_FOLLOWUPS (
	user_id SERIAL,
	followup_id SERIAL,
	PRIMARY KEY (user_id, followup_id));






