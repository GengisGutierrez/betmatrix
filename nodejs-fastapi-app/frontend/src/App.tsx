import { useState, useEffect } from 'react'
import './App.css'

interface Usuario {
  id: number
  nombre: string
}

interface Apuesta {
  id: number
  usuario_id: number
  monto_apostado: number
  resultado: string
  deporte: string
  cuota: number
  descripcion: string
  monto_resultado: number
  created_at: string
}

interface Estadisticas {
  balance_total: number
  total_apostado: number
  apuestas_ganadas: number
  apuestas_perdidas: number
  total_apuestas: number
  porcentaje_exito: number
}

interface FormData {
  monto_apostado: string
  resultado: string
  deporte: string
  cuota: string
  descripcion: string
}

// Datos dummy
const usuariosDummy: Usuario[] = [
  { id: 1, nombre: 'Usuario 1' },
  { id: 2, nombre: 'Usuario 2' },
  { id: 3, nombre: 'Usuario 3' },
  { id: 4, nombre: 'Usuario 4' },
  { id: 5, nombre: 'Usuario 5' },
]

const apuestasDummy: Apuesta[] = [
  {
    id: 1,
    usuario_id: 1,
    monto_apostado: 100,
    resultado: 'Ganancia',
    deporte: 'Fútbol',
    cuota: 2.5,
    descripcion: 'Real Madrid vs Barcelona',
    monto_resultado: 150,
    created_at: '2024-11-01T10:30:00'
  },
  {
    id: 2,
    usuario_id: 1,
    monto_apostado: 50,
    resultado: 'Pérdida',
    deporte: 'Básquet',
    cuota: 1.8,
    descripcion: 'Lakers vs Warriors',
    monto_resultado: -50,
    created_at: '2024-11-02T15:20:00'
  },
  {
    id: 3,
    usuario_id: 1,
    monto_apostado: 75,
    resultado: 'Ganancia',
    deporte: 'Tenis',
    cuota: 3.2,
    descripcion: 'Nadal vs Djokovic',
    monto_resultado: 165,
    created_at: '2024-11-03T18:45:00'
  },
  {
    id: 4,
    usuario_id: 1,
    monto_apostado: 120,
    resultado: 'Pérdida',
    deporte: 'Fútbol',
    cuota: 1.5,
    descripcion: 'PSG vs Bayern',
    monto_resultado: -120,
    created_at: '2024-11-04T20:00:00'
  },
  {
    id: 5,
    usuario_id: 2,
    monto_apostado: 200,
    resultado: 'Ganancia',
    deporte: 'Boxeo',
    cuota: 2.1,
    descripcion: 'Canelo vs GGG',
    monto_resultado: 220,
    created_at: '2024-11-01T22:30:00'
  },
  {
    id: 6,
    usuario_id: 2,
    monto_apostado: 80,
    resultado: 'Ganancia',
    deporte: 'Fútbol',
    cuota: 1.9,
    descripcion: 'Manchester United vs Chelsea',
    monto_resultado: 72,
    created_at: '2024-11-03T16:00:00'
  },
]

function App() {
  const [usuarios] = useState<Usuario[]>(usuariosDummy)
  const [usuarioSeleccionado, setUsuarioSeleccionado] = useState<Usuario | null>(usuariosDummy[0])
  const [apuestas, setApuestas] = useState<Apuesta[]>([])
  const [estadisticas, setEstadisticas] = useState<Estadisticas | null>(null)
  const [apuestaEditando, setApuestaEditando] = useState<Apuesta | null>(null)
  
  const [formData, setFormData] = useState<FormData>({
    monto_apostado: '',
    resultado: 'Ganancia',
    deporte: '',
    cuota: '',
    descripcion: ''
  })

  useEffect(() => {
    if (usuarioSeleccionado) {
      cargarApuestas(usuarioSeleccionado.id)
      cargarEstadisticas(usuarioSeleccionado.id)
    }
  }, [usuarioSeleccionado])

  const cargarApuestas = (usuarioId: number) => {
    const apuestasUsuario = apuestasDummy.filter(a => a.usuario_id === usuarioId)
    setApuestas(apuestasUsuario)
  }

  const cargarEstadisticas = (usuarioId: number) => {
    const apuestasUsuario = apuestasDummy.filter(a => a.usuario_id === usuarioId)
    
    const balance_total = apuestasUsuario.reduce((sum, a) => sum + a.monto_resultado, 0)
    const total_apostado = apuestasUsuario.reduce((sum, a) => sum + a.monto_apostado, 0)
    const apuestas_ganadas = apuestasUsuario.filter(a => a.resultado === 'Ganancia').length
    const apuestas_perdidas = apuestasUsuario.filter(a => a.resultado === 'Pérdida').length
    const total_apuestas = apuestasUsuario.length
    const porcentaje_exito = total_apuestas > 0 
      ? parseFloat(((apuestas_ganadas / total_apuestas) * 100).toFixed(2))
      : 0

    setEstadisticas({
      balance_total,
      total_apostado,
      apuestas_ganadas,
      apuestas_perdidas,
      total_apuestas,
      porcentaje_exito
    })
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      if (apuestaEditando) {
        actualizarApuesta()
      } else {
        agregarApuesta()
      }
    }
  }

  const agregarApuesta = () => {
    if (!formData.monto_apostado || !formData.deporte || !formData.cuota) {
      alert('Por favor completa todos los campos requeridos')
      return
    }

    const monto = parseFloat(formData.monto_apostado)
    const cuota = parseFloat(formData.cuota)
    const monto_resultado = formData.resultado === 'Ganancia' 
      ? monto * cuota - monto
      : -monto

    const nuevaApuesta: Apuesta = {
      id: Math.max(...apuestasDummy.map(a => a.id)) + 1,
      usuario_id: usuarioSeleccionado!.id,
      monto_apostado: monto,
      resultado: formData.resultado,
      deporte: formData.deporte,
      cuota: cuota,
      descripcion: formData.descripcion,
      monto_resultado: monto_resultado,
      created_at: new Date().toISOString()
    }

    apuestasDummy.push(nuevaApuesta)
    cargarApuestas(usuarioSeleccionado!.id)
    cargarEstadisticas(usuarioSeleccionado!.id)
    
    setFormData({
      monto_apostado: '',
      resultado: 'Ganancia',
      deporte: '',
      cuota: '',
      descripcion: ''
    })
  }

  const actualizarApuesta = () => {
    if (!apuestaEditando) return

    const monto = parseFloat(formData.monto_apostado)
    const cuota = parseFloat(formData.cuota)
    const monto_resultado = formData.resultado === 'Ganancia' 
      ? monto * cuota - monto
      : -monto

    const index = apuestasDummy.findIndex(a => a.id === apuestaEditando.id)
    if (index !== -1) {
      apuestasDummy[index] = {
        ...apuestaEditando,
        monto_apostado: monto,
        resultado: formData.resultado,
        deporte: formData.deporte,
        cuota: cuota,
        descripcion: formData.descripcion,
        monto_resultado: monto_resultado
      }
    }

    cargarApuestas(usuarioSeleccionado!.id)
    cargarEstadisticas(usuarioSeleccionado!.id)
    setApuestaEditando(null)
    
    setFormData({
      monto_apostado: '',
      resultado: 'Ganancia',
      deporte: '',
      cuota: '',
      descripcion: ''
    })
  }

  const eliminarApuesta = (id: number) => {
    if (!window.confirm('¿Estás seguro de eliminar esta apuesta?')) return

    const index = apuestasDummy.findIndex(a => a.id === id)
    if (index !== -1) {
      apuestasDummy.splice(index, 1)
    }

    cargarApuestas(usuarioSeleccionado!.id)
    cargarEstadisticas(usuarioSeleccionado!.id)
  }

  const editarApuesta = (apuesta: Apuesta) => {
    setApuestaEditando(apuesta)
    setFormData({
      monto_apostado: apuesta.monto_apostado.toString(),
      resultado: apuesta.resultado,
      deporte: apuesta.deporte,
      cuota: apuesta.cuota.toString(),
      descripcion: apuesta.descripcion || ''
    })
  }

  const cancelarEdicion = () => {
    setApuestaEditando(null)
    setFormData({
      monto_apostado: '',
      resultado: 'Ganancia',
      deporte: '',
      cuota: '',
      descripcion: ''
    })
  }

  const formatearFecha = (fecha: string) => {
    return new Date(fecha).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }

  return (
    <div className="app">
      <div className="sidebar">
        <h2>Usuarios</h2>
        <div className="usuarios-list">
          {usuarios.map(usuario => (
            <div
              key={usuario.id}
              className={`usuario-item ${usuarioSeleccionado?.id === usuario.id ? 'active' : ''}`}
              onClick={() => setUsuarioSeleccionado(usuario)}
            >
              {usuario.nombre}
            </div>
          ))}
        </div>
      </div>

      <div className="main-content">
        {usuarioSeleccionado && (
          <>
            <div className="header">
              <h1>{usuarioSeleccionado.nombre}</h1>
            </div>

            {estadisticas && (
              <div className="estadisticas">
                <div className="stat-card">
                  <h3>Balance Total</h3>
                  <p className={estadisticas.balance_total >= 0 ? 'positive' : 'negative'}>
                    ${estadisticas.balance_total.toFixed(2)}
                  </p>
                </div>
                <div className="stat-card">
                  <h3>Total Apostado</h3>
                  <p>${estadisticas.total_apostado.toFixed(2)}</p>
                </div>
                <div className="stat-card">
                  <h3>Apuestas</h3>
                  <p>{estadisticas.apuestas_ganadas}G / {estadisticas.apuestas_perdidas}P</p>
                </div>
                <div className="stat-card">
                  <h3>% Éxito</h3>
                  <p>{estadisticas.porcentaje_exito}%</p>
                </div>
              </div>
            )}

            <div className="form-container">
              <h3>{apuestaEditando ? 'Editar Apuesta' : 'Nueva Apuesta'}</h3>
              <div className="form-grid">
                <input
                  type="number"
                  name="monto_apostado"
                  placeholder="Monto Apostado"
                  value={formData.monto_apostado}
                  onChange={handleInputChange}
                  onKeyPress={handleKeyPress}
                />
                <select
                  name="resultado"
                  value={formData.resultado}
                  onChange={handleInputChange}
                  onKeyDown={handleKeyPress}
                >
                  <option value="Ganancia">Ganancia</option>
                  <option value="Pérdida">Pérdida</option>
                </select>
                <input
                  type="text"
                  name="deporte"
                  placeholder="Deporte"
                  value={formData.deporte}
                  onChange={handleInputChange}
                  onKeyPress={handleKeyPress}
                />
                <input
                  type="number"
                  step="0.01"
                  name="cuota"
                  placeholder="Cuota/Odds"
                  value={formData.cuota}
                  onChange={handleInputChange}
                  onKeyPress={handleKeyPress}
                />
                <input
                  type="text"
                  name="descripcion"
                  placeholder="Descripción"
                  value={formData.descripcion}
                  onChange={handleInputChange}
                  onKeyPress={handleKeyPress}
                />
              </div>
              <div className="form-actions">
                {apuestaEditando ? (
                  <>
                    <button onClick={actualizarApuesta} className="btn-primary">
                      Actualizar
                    </button>
                    <button onClick={cancelarEdicion} className="btn-secondary">
                      Cancelar
                    </button>
                  </>
                ) : (
                  <button onClick={agregarApuesta} className="btn-primary">
                    Agregar (Enter)
                  </button>
                )}
              </div>
            </div>

            <div className="apuestas-list">
              <h3>Historial de Apuestas</h3>
              {apuestas.length === 0 ? (
                <p className="no-data">No hay apuestas registradas</p>
              ) : (
                <table>
                  <thead>
                    <tr>
                      <th>Fecha</th>
                      <th>Deporte</th>
                      <th>Monto</th>
                      <th>Cuota</th>
                      <th>Resultado</th>
                      <th>Ganancia/Pérdida</th>
                      <th>Descripción</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {apuestas.map(apuesta => (
                      <tr key={apuesta.id}>
                        <td>{formatearFecha(apuesta.created_at)}</td>
                        <td>{apuesta.deporte}</td>
                        <td>${apuesta.monto_apostado.toFixed(2)}</td>
                        <td>{apuesta.cuota.toFixed(2)}</td>
                        <td>
                          <span className={`badge ${apuesta.resultado.toLowerCase()}`}>
                            {apuesta.resultado}
                          </span>
                        </td>
                        <td className={apuesta.monto_resultado >= 0 ? 'positive' : 'negative'}>
                          ${apuesta.monto_resultado.toFixed(2)}
                        </td>
                        <td>{apuesta.descripcion}</td>
                        <td>
                          <button
                            onClick={() => editarApuesta(apuesta)}
                            className="btn-edit"
                          >
                            Editar
                          </button>
                          <button
                            onClick={() => eliminarApuesta(apuesta.id)}
                            className="btn-delete"
                          >
                            Eliminar
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default App