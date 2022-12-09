import React, { useState } from "react";
import { User } from "../../App";
import Login from "./Login";
import "./Login.scss";

interface ModalProps {
	user: User;
	setUser: (user: User) => void;
}
export default function Modal(props: ModalProps) {
	const { setUser } = props;

	const [visible, setVisible] = useState(true);

	return visible ? (
		<div className="modalBackground">
			<div className="modal">
				<Login setUser={setUser} close={() => setVisible(false)} />
			</div>
		</div>
	) : null;
}
