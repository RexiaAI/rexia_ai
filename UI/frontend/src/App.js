import React, { useState, useEffect } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import axios from 'axios';

const ItemTypes = {
  AGENT: 'agent',
  TOOL: 'tool'
};

const DraggableItem = ({ type, name }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type,
    item: { name, type },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }));

  return (
    <div 
      ref={drag} 
      style={{ 
        opacity: isDragging ? 0.5 : 1, 
        cursor: 'move', 
        padding: '10px', 
        border: '1px solid black', 
        marginBottom: '5px',
        backgroundColor: type === ItemTypes.AGENT ? '#ffcccc' : '#ccffcc'
      }}
    >
      {name} ({type})
    </div>
  );
};

const Agency = ({ onDrop, items }) => {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: [ItemTypes.AGENT, ItemTypes.TOOL],
    drop: (item) => onDrop(item),
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
    }),
  }));

  return (
    <div 
      ref={drop} 
      style={{ 
        minHeight: '200px', 
        border: '2px dashed gray', 
        padding: '10px',
        backgroundColor: isOver ? '#f0f0f0' : 'white'
      }}
    >
      <h3>Agency</h3>
      {items.map((item, index) => (
        <div key={index} style={{
          padding: '5px',
          margin: '5px',
          backgroundColor: item.type === ItemTypes.AGENT ? '#ffcccc' : '#ccffcc'
        }}>
          {item.name} ({item.type})
        </div>
      ))}
    </div>
  );
};

function App() {
  const [components, setComponents] = useState({ agents: [], tools: [] });
  const [agencyItems, setAgencyItems] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchComponents = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/components');
        setComponents(response.data);
      } catch (err) {
        setError('Error fetching components. Please try again later.');
        console.error('Error fetching components:', err);
      }
    };

    fetchComponents();
  }, []);

  const handleDrop = (item) => {
    setAgencyItems(prevItems => [...prevItems, item]);
  };

  const handleCreateAgency = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/create_agency', { items: agencyItems });
      console.log('Agency created:', response.data);
      alert('Agency created successfully!');
    } catch (err) {
      setError('Error creating agency. Please try again.');
      console.error('Error creating agency:', err);
    }
  };

  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  return (
    <DndProvider backend={HTML5Backend}>
      <div style={{ display: 'flex', padding: '20px' }}>
        <div style={{ width: '200px', marginRight: '20px' }}>
          <h3>Agents</h3>
          {components.agents.map(agent => (
            <DraggableItem key={agent} type={ItemTypes.AGENT} name={agent} />
          ))}
          <h3>Tools</h3>
          {components.tools.map(tool => (
            <DraggableItem key={tool} type={ItemTypes.TOOL} name={tool} />
          ))}
        </div>
        <div style={{ flex: 1 }}>
          <Agency onDrop={handleDrop} items={agencyItems} />
          <button 
            onClick={handleCreateAgency}
            style={{ marginTop: '20px', padding: '10px', fontSize: '16px' }}
          >
            Create Agency
          </button>
        </div>
      </div>
    </DndProvider>
  );
}

export default App;