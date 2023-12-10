import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import SearchResultItem from './SearchResultItem';
import '../App.css';

const ArticlePage = () => {
  const [article, setArticle] = useState(null);
  const [moreLikeThis, setMoreLikeThis] = useState([]);
  const { articleId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/article/${articleId}`);
        if (!response.ok) {
          throw new Error('Article fetch failed');
        }
        const data = await response.json();
        setArticle(data.article);
        if (data.moreLikeThis) {
          setMoreLikeThis(data.moreLikeThis); // Set moreLikeThis only if it exists
        }
      } catch (error) {
        console.error('Error fetching article:', error);
      }
    };

    if (articleId) {
      fetchArticle();
    }
  }, [articleId]);

  const handleMoreLikeThisClick = (id) => {
    navigate(`/article/${id}`);
  };

  if (!article) {
    return <div>Loading...</div>;
  }

  return (
    <div className="article-page">
      <h1>{article.title}</h1>
      <p>{article.text}</p>
      {moreLikeThis && moreLikeThis.length > 0 && (
        <div className="more-like-this">
          <h2>More Like This</h2>
          {moreLikeThis.map((item) => (
            <SearchResultItem 
              key={item.id}
              id={item.id}
              title={item.title}
              summary={item.summary}
              onClick={() => handleMoreLikeThisClick(item.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default ArticlePage;
