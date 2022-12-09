import { useState } from "react";
import reactLogo from "./assets/react.svg";
import "./App.css";
import Login from "./components/Login/Login";
import Home from "./pages/Home";
import Header from "./components/Header/Header";
import Modal from "./components/Login/Modal";

export interface User {
	id: number;
	username: string;
}
export default function App() {
	const [user, setUser] = useState<User | undefined>(undefined);

	return (
		<div className="App">
			<Header user={user}/>
			<Modal user={user} setUser={setUser}/>
			<Home />
		</div>
	);
}
