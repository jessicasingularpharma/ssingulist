import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

import { AuthLayout } from '@/components/AuthLayout';
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
import { Field } from '@/components/Field';
import { Label } from '@/components/Label';
import { Logo } from '@/components/Logo';
import { Heading } from '@/components/Heading';

const Login = () => {
  const [codigo, setCodigo] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro] = useState('');
  const navigate = useNavigate();
  const { login, user } = useAuth();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setErro('');

    try {
      const sucesso = await login(parseInt(codigo), senha);

      if (sucesso) {
        // Redireciona de acordo com o perfil
        if (user?.is_admin) {
          navigate('/dashboard');
        } else {
          navigate('/ordem-compra/nova');
        }
      } else {
        setErro('Código ou senha inválidos.');
      }
    } catch (err) {
      setErro('Erro inesperado. Tente novamente.');
    }
  };

  return (
    <AuthLayout>
      <form
        onSubmit={handleSubmit}
        className="grid w-full max-w-sm grid-cols-1 gap-6"
      >
        <Logo className="mx-auto" />
        <Heading className="text-center">Acessar sistema</Heading>

        <Field>
          <Label htmlFor="codigo">Código do Funcionário</Label>
          <Input
            id="codigo"
            name="codigo"
            type="number"
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            required
          />
        </Field>

        <Field>
          <Label htmlFor="senha">Senha</Label>
          <Input
            id="senha"
            name="senha"
            type="password"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
          />
        </Field>

        <Button type="submit">Entrar</Button>

        {erro && (
          <p className="text-sm text-red-600 text-center bg-red-100 py-2 rounded">
            {erro}
          </p>
        )}
      </form>
    </AuthLayout>
  );
};

export default Login;
