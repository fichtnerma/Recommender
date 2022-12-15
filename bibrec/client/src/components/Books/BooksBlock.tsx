import { Book } from "./BookItem";
import BookRow from "./BookRow";
import React, { useState } from "react";

interface ItemsBlockProps {
	title: string;
	buttonText?: string;
	items: Book[];
	onItemClick: (book: Book) => void;
}

export function BooksBlock({ title, buttonText = "Mehr laden", items, onItemClick }: ItemsBlockProps) {
	const stepAmount = 5;

	const [currentLimit, setCurrentLimit] = useState(stepAmount);

	const remainingItemsCount = items.length - currentLimit;

	function onButtonClick() {
		if (remainingItemsCount > stepAmount)
			setCurrentLimit(currentLimit + stepAmount);
		else
			setCurrentLimit(currentLimit + remainingItemsCount);
	}

	return <div className={"booksBlockWrapper"}>
		<h2>{title}</h2>
		<BookRow
			onItemClick={onItemClick}
			books={items}
			limit={currentLimit}/>
		{remainingItemsCount ?
			<button onClick={onButtonClick}>{buttonText}</button>
			: null}
	</div>;
}
