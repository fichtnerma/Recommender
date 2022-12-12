import { useEffect, useState } from "react";
import "./App.css";
import Home from "./pages/Home";
import Header from "./components/Header/Header";
import Modal from "./components/Login/Modal";

export type User = UserIdentifiers & UserInfo

interface UserIdentifiers {
	id: number;
	username: string;
}

export interface UserInfo {
	country?: string,
	state?: string,
	city?: string,
	age?: number
}

export default function App() {
	const [user, setUser] = useState<User | undefined>(undefined);
	const [modalVisible, setModalVisible] = useState(true);

	useEffect(() => {
		const userId = sessionStorage.getItem("userId");
		const username = sessionStorage.getItem("username");
		const country = sessionStorage.getItem("country");
		const state = sessionStorage.getItem("state");
		const city = sessionStorage.getItem("city");
		const age = sessionStorage.getItem("age");

		if (userId && username) {
			setUser({
				username,
				id: +userId,
				age: Number(age) || undefined,
				city: city ?? undefined,
				country: country ?? undefined,
				state: state ?? undefined
			});
			setModalVisible(false);
		}
	}, []);

	useEffect(() => {
		if (user) {
			sessionStorage.setItem("userId", user.id.toString());
			sessionStorage.setItem("username", user.username);
			user.country && sessionStorage.setItem("country", user.country);
			user.state && sessionStorage.setItem("state", user.state);
			user.city && sessionStorage.setItem("city", user.city);
			user.age && sessionStorage.setItem("age", user.age.toString());
		}
	}, [user]);

	return (
		<div className="App">
			<Header setVisible={setModalVisible} user={user} setUser={setUser}/>
			{modalVisible ? <Modal visible={modalVisible} setVisible={setModalVisible} setUser={setUser}/> : null}
			<Home user={user}/>
		</div>
	);
}
