import React, { Dispatch, SetStateAction } from "react";
import { User } from "../../App";
import "./Header.scss";

interface HeaderProps {
	user: User | undefined;
	setUser: Dispatch<SetStateAction<User | undefined>>;
	setVisible: (value: boolean) => void;
}

export default function Header({ user, setUser, setVisible }: HeaderProps) {
	function onLogin() {
		setVisible(true);
	}

	function onLogout() {
		setUser(undefined);
		sessionStorage.clear();
		setVisible(true);
	}

	return (
		<header className="header">
			<a className="logoWrapper" href={"/"}>
				<img src="/logo.png" alt="logo"/>
				<h1>BibRec</h1>
			</a>
			<nav>
				<a href="/">Startseite</a>
			</nav>
			<div className={"userManagement"}>{user ? (
				<p>Hallo <strong>{user?.username}</strong>!</p>
			) : null}
				<button onClick={user ? onLogout : onLogin}>{user ? "Abmelden" : "Anmelden"}</button>
			</div>
		</header>
	);
}
