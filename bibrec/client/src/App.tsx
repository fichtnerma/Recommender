import { useEffect, useState } from "react";
import "./App.css";
import Home from "./pages/Home";
import Header from "./components/Header/Header";
import Modal from "./components/Login/Modal";

export type User = UserIdentifiers & UserInfo

interface UserIdentifiers {
	user_id: number;
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
	const [modalVisible, setModalVisible] = useState(false);

	useEffect(() => {
		const userId = sessionStorage.getItem("user_id");
		const username = sessionStorage.getItem("username");
		const country = sessionStorage.getItem("country");
		const state = sessionStorage.getItem("state");
		const city = sessionStorage.getItem("city");
		const age = sessionStorage.getItem("age");

		// TODO: check if backend is up, else logout

		if (userId && username) {
			setUser({
				username,
				user_id: +userId,
				age: Number(age) || undefined,
				city: city ?? undefined,
				country: country ?? undefined,
				state: state ?? undefined
			});
		} else {
			setModalVisible(true)
		}
	}, []);

	return (
		<div className="App">
			<Header setVisible={setModalVisible} user={user} setUser={setUser}/>
			{modalVisible ? <Modal setVisible={setModalVisible} setUser={setUser} user={user}/> : null}
			<Home user={user}/>
		</div>
	);
}
