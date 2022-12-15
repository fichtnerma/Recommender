import React, { useState } from "react";
import BookDetailModal from "../components/BookDetails/BookDetailModal";
import { Book } from "../components/Books/BookItem";
import "./Home.scss";
import { dummyBooks2 } from "../components/Books/mockData";
import { User } from "../App";
import { BooksBlock } from "../components/Books/BooksBlock";

interface HomeProps {
	user?: User;
}

export default function Home({ user }: HomeProps) {
	const [modalVisible, setModalVisible] = useState(false);
	const [selectedBook, setSelectedBook] = useState<undefined | Book>(
		undefined
	);

	function onItemClick(book: Book) {
		setModalVisible(true);
		setSelectedBook(book);
	}

	return (
		<div className="wrapper">
			{modalVisible && selectedBook ? (
				<BookDetailModal
					setSelectedBook={setSelectedBook}
					selectedBook={selectedBook}
					onClose={setModalVisible}
					user={user}
				/>
			) : null}

			{user ? <BooksBlock title={"Deine Empfehlungen"} items={dummyBooks2} onItemClick={onItemClick}/> : null}

			<BooksBlock title={"Top 5 in deinem Land"} items={dummyBooks2} onItemClick={onItemClick}/>

			<BooksBlock title={"Mehr erkunden"} items={dummyBooks2} onItemClick={onItemClick}/>
		</div>
	);
}
