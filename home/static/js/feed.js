function toggleContent(element) {
  const card = element.closest('.post-card');
  const content = card.querySelector('.full-content');

  if (content.style.display === 'none' || content.style.display === '') {
      content.style.display = 'block';
  } else {
      content.style.display = 'none';
  }
}