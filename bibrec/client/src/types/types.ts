export interface Book {
	isbn10: string;
	isbn13: number;
	title: string;
	imageUrlLarge: string;
	imageUrlMedium: string;
	imageUrlSmall: string;
	author: string;
	rating_count: number;
	rating_mean: number;
	pubYear: number;
	publisher: string;
}

export interface Rating {
	userId: number,
	isbn10: string,
	rating: number,
}
