import { CategoryCard, SectionHeading } from "@/entities/stream";
import "./List.css";
import { useRouter } from "next/router";
import { memo } from "react";
const DUMMY_DATA = [
    {
        title: "Chatting",
        views: "21521051",
        category_color: "#9e66ca",
        category_png: "/assets/png_example.png"
    },
    {
        title: "Overwatch",
        views: "15000",
        category_color: "#c94035",
        category_png: "/assets/png_example2.png"
    },
    {
        title: "Apex",
        views: "123214",
        category_color: "#e759ad",
        category_png: "/assets/png_example3.png"
    },
    {
        title: "Movies",
        views: "21422",
        category_color: "#9e66ca",
        category_png: "/assets/png_example3.png"
    }
];

export const RecommendedList = memo(({ onClickCategory }) => {
    return (
        <div className="recommendations-container">
            <SectionHeading>Recommended Categories</SectionHeading>
            <div className="list-container">
                {DUMMY_DATA.map((item) => (
                    <CategoryCard
                        key={item.title}
                        onClick={() => onClickCategory(item.title)}
                        {...item}
                    />
                ))}
            </div>
        </div>
    );
});
