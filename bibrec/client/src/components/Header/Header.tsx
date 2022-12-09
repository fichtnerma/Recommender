import React from "react";
import { User } from "../../App";
import "./Header.scss";

interface HeaderProps {
	user: User;
}
export default function Header(props: HeaderProps) {
	const { user } = props;

	return (
		<header className="header">
			<div className="logoWrapper">
				<img src="/logo.png" alt="logo" />
				<h1>BibRec</h1>
			</div>
			<nav>
				<a href="/">Startseite</a>
				<a href="/">Am Beliebtesten</a>
				<a href="/">Englische Titel</a>
			</nav>
			{user ? (
				<p>
					Hallo <strong>{user?.username}</strong>!
				</p>
			) : null}
		</header>
	);
}
