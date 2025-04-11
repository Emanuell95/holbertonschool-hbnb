document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const priceFilter = document.getElementById('price-filter');
  const loginLink = document.getElementById('login-link');
  const placesList = document.getElementById('places-list');
  const addReview = document.getElementById('add-review');

  if (placesList) {
    placesList.style.display = 'none';
  }

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      await loginUser(email, password);
    });
  }

  checkAuthentication(loginLink, placesList, addReview);

  if (priceFilter) {
    priceFilter.innerHTML = `
      <option value="10">10</option>
      <option value="50">50</option>
      <option value="100">100</option>
      <option value="500">500</option>
      <option value="All">All</option>
    `;
    priceFilter.addEventListener("change", (event) => {
      const selectedPrice = event.target.value;
      filterPlacesByPrice(selectedPrice);
    });
  }

  const placeId = getPlaceIdFromUrl();
  if (placeId) {
    const token = getCookie('token');
    if (token) {
      fetchPlaceDetails(placeId, token);
    }
  }
});

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
}

function checkAuthentication(loginLink, placesList, addReview) {
  const token = getCookie('token');
  if (token) {
    loginLink.style.display = 'none';
    if (placesList) {
      placesList.style.display = 'none';
    }
    if (addReview) {
      addReview.style.display = 'none';
    }
    fetchPlaces(token);
  } else {
    loginLink.style.display = 'none';
    if (placesList) {
      placesList.style.display = 'flex';
    }
    if (addReview) {
      addReview.style.display = 'flex';
    }
  }
}

async function loginUser(email, password) {
  try {
    const response = await fetch('https://localhost:5000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;
      window.location.href = 'index.html';
    } else {
      const errorData = await response.json();
      alert('Login failed: Invalid email or password');
    }
  } catch (error) {
    alert('Login failed: ' + error.message);
  }
}

async function fetchPlaces(token) {
  try {
    const response = await fetch('https://localhost:5000/api/places', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    } else {
      alert('Failed to fetch places');
    }
  } catch (error) {
    alert('Failed to fetch places: ' + error.message);
  }
}

function displayPlaces(places) {
  const placesList = document.querySelector('#places-list');
  placesList.innerHTML = '';

  if (places.length === 0) {
    placesList.innerHTML = '<p>No places found.</p>';
    return;
  }

  const list = document.createElement('ul');
  list.classList.add('places-list');

  places.forEach(place => {
    const li = document.createElement('li');
    li.classList.add('place-card');
    li.innerHTML = `
      <h2>${place.title || 'No title available'}</h2>
      <p> Price per night: ${place.price || 'No price available'}</p>
      <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
    `;
    list.appendChild(li);
  });
  placesList.appendChild(list);
}

function filterPlacesByPrice(selectedPrice) {
  const placesList = document.querySelector('#places-list');
  const placeCards = Array.from(placesList.querySelectorAll('.place-card'));
  placeCards.forEach(placeCard => {
    const priceText = placeCard.querySelector('p').textContent;
    const price = parseInt(priceText.replace("Price per night: $", "").trim());
    if (selectedPrice === 'All' || price <= selectedPrice) {
      placeCard.style.display = 'flex';
    } else {
      placeCard.style.display = 'none';
    }
  });
}

function getPlaceIdFromUrl() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('id');
}

async function fetchPlaceDetails(placeId, token) {
  try {
    const response = await fetch(`https://localhost:5000/api/places/${placeId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
    } else {
      alert('Failed to fetch place details');
    }
  } catch (error) {
    alert('Failed to fetch place details: ' + error.message);
  }
}

function displayPlaceDetails(place) {
  const placeDetailsContainer = document.getElementById('place-details');
  placeDetailsContainer.innerHTML = `
    <h1>${place.title || 'No title available'}</h1>
    <p><strong>Price:</strong> ${place.price || 'No price available'}</p>
    <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
    <p><strong>Amenities:</strong> ${place.amenities?.name || 'No amenities available'}</p>
    <div id="reviews">
      <h2>Reviews</h2>
      ${place.reviews?.map(review => `
        <div class="review-card">
          <p>Rating: ${review.rating}</p>
          <p>${review.text}</p>
        </div>
      `).join('') || 'No reviews available'}
    </div>
  `;
}

const addReviewSection = document.getElementById('add-review');
if (addReviewSection) {
  addReviewSection.innerHTML = `
    <h2>Add a Review</h2>
    <form id="review-form">
      <label for="rating">Rating: (1-5):</label>
      <input type="number" id="rating" name="rating" min="1" max="5" required>
      <br>
      <label for="comment">Comment:</label>
      <textarea id="comment" name="comment" required></textarea>
      <br>
      <button type="submit">Submit</button>
    </form>
  `;
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const rating = document.getElementById('rating').value;
      const comment = document.getElementById('comment').value;
      const placeId = getPlaceIdFromUrl();
      const token = getCookie('token');
      if (!token) {
        window.location.href = 'index.html';
        return;
      }
      try {
        const response = await fetch(`https://localhost:5000/api/places/${placeId}/reviews`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ rating, comment })
        });

        if (response.ok) {
          alert('Review submitted successfully');
          window.location.href = 'index.html';
        } else {
          alert('Failed to submit review');
        }
      } catch (error) {
        alert('Failed to submit review: ' + error.message);
      }
    });
  }
}