import React, { Dispatch, SetStateAction } from "react";
import { User } from "../../App";
import Login from "./Login";
import "./Login.scss";

interface ModalProps {
	user?: User;
	setUser: Dispatch<SetStateAction<User | undefined>>;
	setVisible: (value: boolean) => void;
}

export default function Modal({ setUser, setVisible, user }: ModalProps) {
	return <div className="modalBackground">
		<div className="modal">
			<Login setUser={setUser as Dispatch<SetStateAction<User>>} close={() => setVisible(false)} user={user}/>
		</div>
	</div>;
}
