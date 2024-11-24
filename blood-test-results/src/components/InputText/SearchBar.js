import React, { useState } from 'react';

const SearchBox = ( {updateFunction} ) => {
  const [searchQuery, setSearchQuery] = useState('');

  // Handle input changes
  const handleInputChange = (event) => {
    setSearchQuery(event.target.value);
  };

  // You can handle the search logic here
  const handleSearch = () => {
    console.log("Searching for:", searchQuery);
    // Add search logic here (e.g., filter items, make API call, etc.)
    fetch(`http://127.0.0.1:5000/subject/${searchQuery}`).then(
      res => res.json()
    ).then(
      data => {
        updateFunction(data)
        console.log(data)
        // console.log(data)
      }
    )
  };

  return (
    <div>
      <input
        type="text"
        value={searchQuery}
        onChange={handleInputChange}
        placeholder="Enter Subject ID"
        aria-label="Search"
        className="text-black border-slate-300 border-2 rounded-lg"
      />
      <button
      onClick={handleSearch}
      className="rounded-lg px-1 py-1"
      >
      Go
    </button>
    </div>
  );
};

export default SearchBox;
