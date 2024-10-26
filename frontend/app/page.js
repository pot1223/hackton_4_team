'use client';

import Image from "next/image";
import { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleRight, faAngleLeft } from '@fortawesome/free-solid-svg-icons';
import Header from './components/Header';
import BookCard from './components/BookCard';

const books = [
  { id: 1, title: '채식주의자', topic: '자본주의', image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg' },
  { id: 2, title: '친환경에너지', topic: 'topic2', image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg' },
  { id: 3, title: '금리인하', topic: '청년', image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg' },
  { id: 4, title: 'K-Pop', topic: 'test', image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg' },
  { id: 5, title: '첨단기술', topic: 'test', image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg' },
  { id: 6, title: '우주과학', topic: 'test', image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg' },
  { id: 7, title: '의학과 미래', topic: 'test', image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg' },
  { id: 8, title: '로봇공학', topic: 'test', image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg' },
  { id: 9, title: '환경 보호', topic: 'test', image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg' },
  { id: 10, title: '예술과 문화', topic: 'test', image: 'https://contents.kyobobook.co.kr/sih/fit-in/300x0/pdt/9788936434595.jpg' },
];

export default function Home() {
  const [index, setIndex] = useState(0); // 현재 첫 번째 책의 인덱스
  const [visibleBooks, setVisibleBooks] = useState(4); // 한 번에 보이는 책 개수

  // 화면 크기에 따라 보이는 책 개수 조정
  useEffect(() => {
    const updateVisibleBooks = () => {
      const width = window.innerWidth;
      if (width >= 1370) setVisibleBooks(4);
      else if (width >= 1024) setVisibleBooks(3);
      else if (width >= 768) setVisibleBooks(2);
      else setVisibleBooks(1);
    };

    window.addEventListener('resize', updateVisibleBooks);
    updateVisibleBooks(); // 초기 화면 크기 설정

    return () => window.removeEventListener('resize', updateVisibleBooks);
  }, []);
  const handleNext = () => {
    if (index + visibleBooks < books.length) {
      setIndex(index + 1);
    }
  };

  const handlePrev = () => {
    if (index > 0) {
      setIndex(index - 1);
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '40px', position: 'relative' }}>
      <h1 style={{ fontSize: '48px', color: '#4a5a31', paddingTop: '24px', paddingBottom: '8px' }}>금주의 독립서적 큐레이션</h1>
      <h2 style={{ fontsize: '24px', paddingBottom: '16px', fontWeight: 'normal' }}>최근 흐름과 맞닿은 주제들로 엄선한 책을 추천해드려요.</h2>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        gap: '20px', // 화살표와 책 사이 간격 조정
        width: '80%',
        margin: '0 auto',
      }}>
        <button onClick={handlePrev} disabled={index === 0} style={{
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          fontSize: '24px',
        }}>
          <FontAwesomeIcon icon={faAngleLeft} size="2x" />
        </button>

        <div style={{ 
          display: 'flex',
          justifyContent: 'center',
          gap: '20px',
          overflow: 'hidden', 
          }}
        >
          {books.slice(index, index + visibleBooks).map((book) => (
            <BookCard key={book.id} book={book} />
          ))}
        </div>
        <button onClick={handleNext} disabled={index + visibleBooks >= books.length} style={{
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          fontSize: '24px', 
        }}
        >
          <FontAwesomeIcon icon={faAngleRight} size="2x" />
        </button>
      </div>
    </div>
  );
}
