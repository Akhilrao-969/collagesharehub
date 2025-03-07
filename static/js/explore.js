
document.addEventListener('DOMContentLoaded', function() {
    // Grid/List view toggle
    const gridViewBtn = document.getElementById('gridViewBtn');
    const listViewBtn = document.getElementById('listViewBtn');
    const productGrid = document.querySelector('.product-grid');
    
    // Load preferred view from localStorage if available
    const currentView = localStorage.getItem('viewPreference') || 'grid';
    if (currentView === 'list') {
        productGrid.classList.add('list-view');
        gridViewBtn.classList.remove('btn-dark');
        gridViewBtn.classList.add('btn-outline-dark');
        listViewBtn.classList.remove('btn-outline-dark');
        listViewBtn.classList.add('btn-dark');
    }
    
    // Grid view button click
    gridViewBtn.addEventListener('click', function() {
        productGrid.classList.remove('list-view');
        gridViewBtn.classList.remove('btn-outline-dark');
        gridViewBtn.classList.add('btn-dark');
        listViewBtn.classList.remove('btn-dark');
        listViewBtn.classList.add('btn-outline-dark');
        localStorage.setItem('viewPreference', 'grid');
    });
    
    // List view button click
    listViewBtn.addEventListener('click', function() {
        productGrid.classList.add('list-view');
        listViewBtn.classList.remove('btn-outline-dark');
        listViewBtn.classList.add('btn-dark');
        gridViewBtn.classList.remove('btn-dark');
        gridViewBtn.classList.add('btn-outline-dark');
        localStorage.setItem('viewPreference', 'list');
    });
});
