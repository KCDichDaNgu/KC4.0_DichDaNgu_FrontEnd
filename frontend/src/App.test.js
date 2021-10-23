/* eslint-disable no-undef */
/* eslint-disable import/no-unresolved */
import React from 'react';
import { render, screen, fireEvent } from './helpers/test-utils';
import App from './App';
import TranslateScreen from './screens/TranslationScreen';

// ? Queries: many types of query (Get, Find, Query). 
// After selecting an element, you can use the Events API or User-event.

test('Hiện tiêu đề', () => {
	render(<App />);
	const linkElement = screen.getByText(/UET Dịch máy đa ngôn ngữ/i);
	expect(linkElement).toBeInTheDocument();
});

test('Chưa ấn vào nút Tài liệu thì chưa hiện ra nút chọn mà hình', () => {
	render(<TranslateScreen />);
	const text = screen.queryByText(/Chọn tài liệu/);
	expect(text).toBeNull();
});

test('Ấn vào nút Tài liệu hiện ra nút chọn mà hình', () => {
	render(<TranslateScreen />);
	// This will search for all elements that have a text node with text matching the given text.
	const button = screen.getByText(/Tài liệu/);
	fireEvent.click(button);
	expect(screen.getByText(/Chọn tài liệu/)).toBeInTheDocument();
});